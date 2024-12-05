import os
import json

from azureml.studio.core.io.model_directory import ModelDirectory
from pathlib import Path
from azureml.studio.modules.ml.score.assign_data_to_clusters.assign_data_to_clusters import AssignDataToClustersModule
from azureml.designer.serving.dagengine.converter import create_dfd_from_dict
from collections import defaultdict
from azureml.designer.serving.dagengine.utils import decode_nan
from azureml.studio.common.datatable.data_table import DataTable


model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'trained_model_outputs')
schema_file_path = Path(model_path) / '_schema.json'
with open(schema_file_path) as fp:
    schema_data = json.load(fp)


def init():
    global model
    model = ModelDirectory.load(model_path).model


def run(data):
    data = json.loads(data)
    input_entry = defaultdict(list)
    for row in data:
        for key, val in row.items():
            input_entry[key].append(decode_nan(val))

    data_frame_directory = create_dfd_from_dict(input_entry, schema_data)
    score_module = AssignDataToClustersModule()
    result, = score_module.run(
        cluster=model,
        data_table=DataTable.from_dfd(data_frame_directory),
        append_or_result_only=True)
    return json.dumps({"result": result.data_frame.values.tolist()})
