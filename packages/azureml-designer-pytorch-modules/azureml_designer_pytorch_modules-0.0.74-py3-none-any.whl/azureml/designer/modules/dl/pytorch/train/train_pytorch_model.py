import importlib

import argparse
import torch
from torchvision import transforms as t

from azureml.designer.core.model.builtin_models.pytorch.state_dict import PytorchStateDictModel
from azureml.designer.core.model.constants import ModelSpecConstants
from azureml.designer.core.model.model_spec.builtin_model_meta.model_input import ModelInput
from azureml.designer.core.model.model_spec.builtin_model_meta.pre_processor import ImageNormalizer
from azureml.designer.core.model.model_spec.builtin_model_meta.task_type import TaskType
from azureml.designer.modules.dl.pytorch.train.trainer import trainer
from azureml.studio.core.io.image_directory import ImageDirectory
from azureml.studio.core.io.image_schema import ImageAnnotationTypeName
from azureml.studio.core.io.model_directory import ModelDirectory, save_pytorch_state_dict_model
from azureml.studio.core.logger import TimeProfile, logger
from azureml.studio.core.error import InvalidDirectoryError
from azureml.studio.internal.error import (ErrorMapping, InvalidDatasetError,
                                           NotLabeledDatasetError, InvalidModelDirectoryError)
from azureml.studio.internal.error_handler import ErrorHandler
from azureml.designer.modules.dl.pytorch.model_deployment.model_deployment_handler import PytorchModelDeploymentHandler
from azureml.designer.modules.dl.pytorch.package_info import PACKAGE_NAME, VERSION
from azureml.designer.modules.dl.pytorch.train.trainer.trainer_utils import (DistributedConfig, init_distributed_mode,
                                                                             is_first_rank)

MEAN = [0.5, 0.5, 0.5]
STD = [0.5, 0.5, 0.5]
NORMALIZATION = {'mean': MEAN, 'std': STD}

TASKTYPE_TRAINER_MAPPING = {TaskType.MultiClassification.name: trainer.ClassificationTrainer.__name__}


def get_tensor_transform(ann_type):
    '''Get tensor transform/transforms based on annotation type.

    :param ann_type: str
    :return: (transforms.Compose, transforms.Compose)
    '''
    # 'transform' refers to a function/transform that takes in an PIL image
    # and returns a transformed version. E.g, transforms.ToTensor.
    transform = None
    # 'target_tranform' refers to a function/transform that takes in the target and transforms it.
    target_transform = None
    # transforms refers to a function/transform that takes input sample and its target as entry
    # and returns a transformed version.
    transforms = None
    if ann_type == ImageAnnotationTypeName.CLASSIFICATION:
        # Normalize to (-1, 1).
        transform = t.Compose([
            t.ToTensor(),
            t.Normalize(**NORMALIZATION),
        ])
    # TODO: support other kind of annotation type

    return transform, target_transform, transforms


def load_dataset(data_path):
    try:
        data_dir = ImageDirectory.load(data_path)
        ann_type = data_dir.get_annotation_type()
    except ValueError as e:
        if "no valid image is provided" in str(e.args).lower():
            ErrorMapping.rethrow(
                e,
                InvalidDatasetError(
                    dataset1=data_path,
                    reason=f"Got exception when loading: {ErrorMapping.get_exception_message(e)}",
                    troubleshoot_hint="Please make sure all images in input dataset are valid, see "
                    "https://aka.ms/aml/convert-to-image-directory for input image dataset requirement."))
        else:
            ErrorMapping.rethrow(e, NotLabeledDatasetError(
                dataset_name=data_dir.basedir,
                troubleshoot_hint="See https://aka.ms/aml/convert-to-image-directory and "
                "prepare a labeled image dataset for training."))

    logger.info(f'Got annotation type: {ann_type}')
    transform, target_transform, transforms = get_tensor_transform(ann_type)
    dataset = data_dir.to_torchvision_dataset(transform=transform,
                                              target_transform=target_transform,
                                              transforms=transforms)
    logger.info(f'Dataset classes: {dataset.classes}')
    return dataset, ann_type


def check_dataset(train_set, valid_set, train_ann_type, valid_ann_type):
    # TODO: validate if train and valid set have different ann type when there are tasks
    # of other kind of annotation types.
    if torch.distributed.is_initialized():
        world_size = torch.distributed.get_world_size()
        # Compared to twice data set count because DistributedSampler will add extra samples automatically,
        # but twice is the largest scope it can handle.
        ErrorMapping.verify_less_than_or_equal_to(
            value=world_size, b=2*len(train_set), arg_name='World size', b_name='twice train data count')
        ErrorMapping.verify_less_than_or_equal_to(
            value=world_size, b=2*len(valid_set), arg_name='World size', b_name='twice valid data count')

    if len(set(valid_set.classes).difference(set(train_set.classes))) > 0:
        ErrorMapping.throw(InvalidDatasetError(
            dataset1='Validation dataset',
            reason="categories of validation dataset are different from that of training dataset",
            troubleshoot_hint="Please make sure training and validation dataset have the same categories."))


def init_model(untrained_model_path, num_classes):
    logger.info("Start building model.")
    try:
        untrained_model_directory = ModelDirectory.load_instance(untrained_model_path, PytorchStateDictModel)
    except InvalidDirectoryError as e:
        ErrorMapping.rethrow(e, InvalidModelDirectoryError(
            arg_name=untrained_model_path, reason=e.reason,
            troubleshoot_hint='Please make sure input untrained model is pytorch model.'))

    task_type = untrained_model_directory.task_type
    flavor_extras = untrained_model_directory.model_meta.flavor_extras
    model_module_name = flavor_extras.get(ModelSpecConstants.MODEL_MODULE_KEY, None)
    model_module = importlib.import_module(model_module_name)
    model_class_name = flavor_extras.get(ModelSpecConstants.MODEL_CLASS_KEY, None)
    model_class = getattr(model_module, model_class_name)
    init_params = flavor_extras.get(ModelSpecConstants.INIT_PARAMS_KEY, {})
    init_params['num_classes'] = num_classes
    logger.info(f'Init model class {model_class} with parameter setting {init_params}.')
    model = model_class(**init_params)
    return model, init_params, task_type


def init_deployment_handler(train_data_path):
    with TimeProfile("Create deployment handler and inject schema and sample."):
        image_directory = ImageDirectory.load(train_data_path)
        deployment_handler = PytorchModelDeploymentHandler()
        deployment_handler.data_schema = image_directory.schema
        deployment_handler.sample_data = image_directory.get_samples()
    return deployment_handler


def save_trained_model(trained_model_path, best_model, init_params, class_to_idx, task_type, deployment_handler):
    id_to_class_dict = dict((v, k) for k, v in class_to_idx.items())
    pre_processor = ImageNormalizer(**NORMALIZATION)
    model_input = ModelInput(name='image', pre_processor=pre_processor)
    logger.info(f'Saving trained model {trained_model_path}')
    save_pytorch_state_dict_model(
        save_to=trained_model_path,
        pytorch_model=best_model,
        init_params=init_params,
        inputs=[model_input],
        task_type=task_type,
        label_map=id_to_class_dict,
        deployment_handler=deployment_handler,
    )


@ErrorHandler(save_module_statistics=is_first_rank())
def entrance(untrained_model_path,
             train_data_path,
             valid_data_path,
             trained_model_path,
             epochs=2,
             batch_size=4,
             num_warmup_steps=0,
             learning_rate=0.001,
             random_seed=231,
             patience=3,
             print_freq=100,
             distributed=False,
             rank=None,
             world_size=None,
             local_rank=None,
             dist_url=None):
    # Add package version log
    logger.info(f'{PACKAGE_NAME} {VERSION}')
    if distributed:
        init_distributed_mode(rank=rank, world_size=world_size, local_rank=local_rank,
                              dist_url=dist_url)
    else:
        logger.info('Cannot start distributed training. Please use multiple GPUs to activate.')

    train_set, train_ann_type = load_dataset(train_data_path)
    valid_set, valid_ann_type = load_dataset(valid_data_path)
    check_dataset(train_set, valid_set, train_ann_type, valid_ann_type)
    train_sampler = torch.utils.data.distributed.DistributedSampler(
        train_set) if torch.distributed.is_initialized() else None
    valid_sampler = torch.utils.data.distributed.DistributedSampler(
        valid_set) if torch.distributed.is_initialized() else None
    # 'num_classes' will be used in model initialization.
    num_classes = train_set.num_of_classes
    model, init_params, task_type = init_model(untrained_model_path, num_classes)
    trainer_class = getattr(trainer, TASKTYPE_TRAINER_MAPPING[task_type.name], None)
    logger.info(f'Use trainer {trainer_class} for task type {task_type}.')
    task = trainer_class(model)
    with TimeProfile("Starting training"):
        best_model = task.fit(train_set=train_set,
                              train_sampler=train_sampler,
                              valid_set=valid_set,
                              valid_sampler=valid_sampler,
                              epochs=epochs,
                              batch_size=batch_size,
                              num_warmup_steps=num_warmup_steps,
                              lr=learning_rate,
                              random_seed=random_seed,
                              patience=patience,
                              print_freq=print_freq)
    # Synchronizes all processes to avoid "Broken Pipe" runtime error.
    # This error usually occurs in unfinished processes if master process completes first.
    if torch.distributed.is_initialized():
        torch.distributed.barrier()

    deployment_handler = init_deployment_handler(train_data_path)
    if is_first_rank():
        # All processes should see same parameters as they all start from same
        # random parameters and gradients are synchronized in backward passes.
        # Therefore, saving it in one process is sufficient.
        save_trained_model(
            trained_model_path=trained_model_path,
            best_model=best_model.module if distributed else best_model,
            init_params=init_params,
            class_to_idx=train_set.class_to_idx,
            task_type=task_type,
            deployment_handler=deployment_handler,
        )


def parse_args():
    parser = argparse.ArgumentParser(description='Train pytorch model.')
    parser.add_argument("--untrained-model-path", nargs='?', type=str, help="Path to the untrained model")
    parser.add_argument("--train-data-path", nargs='?', type=str, help="Path to the train data")
    parser.add_argument("--valid-data-path", nargs='?', type=str, help="Path to the valid data")
    parser.add_argument("--trained-model-path", nargs='?', type=str, help="Path to the trained model")
    parser.add_argument("--epochs", nargs='?', type=int, default=2, help="epochs")
    parser.add_argument("--batch-size", nargs='?', type=int, default=4, help="batch size")
    parser.add_argument("--num-warmup-steps", nargs='?', type=int, default=0, help="warmup step number")
    parser.add_argument("--learning-rate", nargs='?', type=float, default=0.001, help="learning rate")
    parser.add_argument("--random-seed", nargs='?', type=int, default=231, help="random seed")
    parser.add_argument("--patience", nargs='?', type=int, default=3, help="early stopping rounds")
    parser.add_argument("--print-freq", nargs='?', type=int, default=100, help="log print frequency")
    args = parser.parse_args()
    dist_conf = DistributedConfig.create()
    args.distributed, args.rank, args.world_size, args.local_rank, args.dist_url = dist_conf.distributed, \
        dist_conf.rank, dist_conf.world_size, dist_conf.local_rank, dist_conf.dist_url
    return args


if __name__ == '__main__':
    entrance(**vars(parse_args()))
