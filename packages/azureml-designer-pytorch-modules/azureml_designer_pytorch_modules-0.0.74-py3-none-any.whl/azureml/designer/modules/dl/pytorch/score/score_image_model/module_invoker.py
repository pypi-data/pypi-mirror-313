import click
from azureml.designer.modules.dl.pytorch.score.score_image_model.score_image_model import ScoreImageModel
from azureml.studio.core.error import _OPEN_SUPPORT_TICKET_HINT
from azureml.studio.core.logger import get_logger, TimeProfile
from azureml.studio.core.io.image_directory import ImageDirectory
from azureml.studio.core.io.model_directory import ModelDirectory
from azureml.studio.core.utils.fileutils import ensure_folder
from azureml.studio.internal.error_handler import error_handler
from azureml.studio.internal.error import InvalidModelDirectoryError
from azureml.designer.modules.dl.pytorch.package_info import PACKAGE_NAME, VERSION

# using because __name__ is '__main__', which violates the requirement of get_logger,
# which only accepts lower case letters
logger = get_logger('module_invoker')


@click.command()
@click.option("--trained-model", help="Path to ModelDirectory")
@click.option("--dataset", help="Path to ImageDirectory")
@click.option("--scored-dataset", help="Path to output DataFrameDirectory")
@error_handler
def entrance(trained_model: str, dataset: str, scored_dataset: str):
    # Add package version log
    logger.info(f'{PACKAGE_NAME} {VERSION}')

    score_module = ScoreImageModel()
    with TimeProfile("Loading input_data_directory"):
        input_image_directory = ImageDirectory.load(dataset)
    with TimeProfile("Loading input_model_directory"):
        if ModelDirectory.is_legacy_pickle_model(trained_model):
            raise InvalidModelDirectoryError(
                arg_name=trained_model,
                reason="Got legacy pickle model",
                troubleshoot_hint="This error usually occurs when you connect a traditional ML model to "
                                  "'Score Image Model', in which case please use 'Score Model' instead")
        try:
            input_model_directory = ModelDirectory.load_with_generic_model(
                load_from_dir=trained_model,
                install_dependencies=False)
        except BaseException as e:
            raise InvalidModelDirectoryError(
                arg_name=trained_model,
                reason="Failed to load generic model",
                troubleshoot_hint="This error usually occurs when you have invalid generic model content in the "
                                  "ModelDirectory, please make sure that it contains the required dependencies in "
                                  "conda.yaml. It could also be caused by error in dependency installation, "
                                  "please check the pip and conda dependency installation log and retry if it's "
                                  f"transient network error. {_OPEN_SUPPORT_TICKET_HINT}"
            ) from e
    with TimeProfile("Running score_module.on_init"):
        score_module.on_init(
            trained_model=input_model_directory,
            dataset=input_image_directory
        )
    with TimeProfile("Running score_module.run"):
        output_dfd, = score_module.run(
            trained_model=input_model_directory,
            dataset=input_image_directory
        )
    with TimeProfile(f"Dumping DataFrameDirectory to {scored_dataset}"):
        ensure_folder(scored_dataset)
        output_dfd.dump(scored_dataset)


if __name__ == "__main__":
    entrance()
