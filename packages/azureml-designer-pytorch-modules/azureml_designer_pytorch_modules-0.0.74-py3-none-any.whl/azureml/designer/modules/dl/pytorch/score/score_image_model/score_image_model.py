import multiprocessing
from itertools import islice
from typing import Generator, Tuple

import pandas as pd
from azureml.designer.core.model.builtin_models.builtin_model import BuiltinModel
from azureml.designer.core.model.extended_column_types import ExtendedColumnTypeName
from azureml.designer.core.model.model_spec.builtin_model_meta.task_type import TaskType
from azureml.studio.core.data_frame_schema import DataFrameSchema
from azureml.studio.core.io.image_directory import ImageDirectory
from azureml.studio.core.io.data_frame_directory import DataFrameDirectory
from azureml.studio.core.io.model_directory import ModelDirectory
from azureml.studio.core.logger import get_logger
from azureml.designer.modules.dl.pytorch.common.pytorch_utils import raise_error
from azureml.designer.modules.dl.pytorch.score.schema import generate_score_column_meta

logger = get_logger(__name__)


class ScoreImageModel(object):

    def __init__(self):
        logger.info(f"Init ScoreImageModel")
        self._model = None
        # Use cpu count as batch size for parallelism
        self._batch_size = multiprocessing.cpu_count()
        logger.info(f"Stack image into batches of size {self._batch_size}")

    def on_init(self,
                trained_model: ModelDirectory,
                dataset: ImageDirectory) -> None:
        self._model = trained_model.generic_model

    def run(self,
            trained_model: ModelDirectory,
            dataset: ImageDirectory
            ) -> Tuple[DataFrameDirectory, ]:
        if not isinstance(dataset, ImageDirectory):
            raise Exception(f"Unsupported dataset type: {type(dataset)}, expecting ImageDirectory")
        predict_result_df = pd.DataFrame()
        non_feature_df = pd.DataFrame()
        feature_columns_names = [column.name for column in dataset.schema_instance.column_attributes
                                 if column.is_feature]
        for batch_index, (batch_df, columns_types) in enumerate(self._batching(dataset)):
            logger.debug(f"Scoring batch {batch_index}.")
            batch_non_feature_df = batch_df.loc[:, batch_df.columns.difference(feature_columns_names)]
            non_feature_df = pd.concat([non_feature_df, batch_non_feature_df], ignore_index=True)
            try:
                batch_predict_result, _ = self._model.predict(batch_df[feature_columns_names], columns_types)
            except Exception as e:
                raise_error(e, mode='Testing')

            predict_result_df = pd.concat([predict_result_df, batch_predict_result], ignore_index=True)

        result_df = pd.concat([non_feature_df, predict_result_df], axis=1)
        logger.debug(f"result_df =\n{result_df}")

        # TODO: Let ModelSDK provide syntax sugar
        if isinstance(self._model.core_model, BuiltinModel) and \
                self._model.core_model.task_type == TaskType.MultiClassification:
            score_columns = generate_score_column_meta(predict_df=result_df)
            schema_init_params = {
                'column_attributes': DataFrameSchema.generate_column_attributes(df=result_df),
                'score_column_names': score_columns
            }
            # Workaround until ImageDirectory provide method that doesn't throw if non-exist
            try:
                schema_init_params['label_column_name'] = dataset.get_annotation_column()
            except BaseException:
                logger.warning(f"Failed to get ground_truth_column from ImageDirectory", exc_info=True)
            meta_data = DataFrameSchema(**schema_init_params)
            dfd = DataFrameDirectory.create(data=result_df, schema=meta_data.to_dict())
        else:
            dfd = DataFrameDirectory.create(data=result_df)
        return dfd,

    def _batching(self, input_image_directory: ImageDirectory) -> Generator:
        """Batch input_data into DataFrames.
        Return a generator generates a DataFrame of columns:
        ["category", "image_id", "label", "image"] with self.batch_size rows.

        :param input_image_directory: ImageDirectory
        :return: generator of (DataFrame, columns_types)
        """
        columns_types = {}
        # Fill the gap between column_attributes of core and column_type of model_sdk
        for column in input_image_directory.schema_instance.column_attributes:
            if column.column_type == "Bytes" and column.properties.get('mime_type', '').startswith('image'):
                columns_types[column.name] = ExtendedColumnTypeName.IMAGE
            else:
                columns_types[column.name] = column.column_type
        image_iterator = input_image_directory.iter_images()
        rows = list(islice(image_iterator, self._batch_size))
        while rows:
            yield pd.DataFrame(rows), columns_types
            rows = list(islice(image_iterator, self._batch_size))
