import os
import json

from azureml.studio.core.io.model_directory import ModelDirectory
from pathlib import Path
from azureml.designer.modules.dl.pytorch.score.score_image_model.score_image_model import ScoreImageModel
from azureml.designer.serving.dagengine.converter import create_imd_from_dict
from collections import defaultdict
from azureml.designer.serving.dagengine.utils import decode_nan


model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'trained_model_outputs')
schema_file_path = Path(model_path) / '_schema.json'
with open(schema_file_path) as fp:
    schema_data = json.load(fp)


def init():
    global model_directory
    model_directory = ModelDirectory.load(model_path)


def run(data):
    data = json.loads(data)
    input_entry = defaultdict(list)
    for row in data:
        for key, val in row.items():
            input_entry[key].append(decode_nan(val))

    image_directory = create_imd_from_dict(input_entry, schema_data)
    score_module = ScoreImageModel()
    score_module.on_init(model_directory, image_directory)
    result, = score_module.run(model_directory, image_directory)
    return json.dumps({"result": result.data.values.tolist()})
