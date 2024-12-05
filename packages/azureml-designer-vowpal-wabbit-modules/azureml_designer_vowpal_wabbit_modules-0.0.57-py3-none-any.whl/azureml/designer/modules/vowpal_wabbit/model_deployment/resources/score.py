import os
import json
from collections import defaultdict
from pathlib import Path

from azureml.studio.core.io.model_directory import ModelDirectory
from azureml.designer.serving.dagengine.utils import decode_nan
from azureml.designer.modules.vowpal_wabbit.score_vowpal_wabbit_model.score_vowpal_wabbit_model import \
    ScoreVowpalWabbitModelModule
from azureml.designer.serving.dagengine.converter import create_dfd_from_dict


model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'trained_model_outputs')
schema_file_path = Path(model_path) / '_schema.json'


if schema_file_path.exists():
    # if schema not exists, the model is trained with AnyDirectory
    with open(schema_file_path) as fp:
        schema_data = json.load(fp)
else:
    schema_data = None


def init():
    global model
    model = ModelDirectory.load(load_from_dir=model_path)


def run(data):
    data = json.loads(data)
    input_entry = defaultdict(list)
    for row in data:
        for key, val in row.items():
            input_entry[key].append(decode_nan(val))

    data_frame_directory = create_dfd_from_dict(input_entry, schema_data)
    score_params = dict(
        trained_vowpal_wabbit_model=model,
        test_data=data_frame_directory,
        vw_arguments='--link logistic',
        include_an_extra_column_containing_labels=True,
        include_an_extra_column_containing_raw_scores=True,
        specify_file_type="VW")

    result_dfd, = ScoreVowpalWabbitModelModule().run(**score_params)
    result_df = result_dfd.data
    return json.dumps(result_df.to_dict("list"))
