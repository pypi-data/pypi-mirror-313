import json
from .visio_model import VisioModel


def load_file(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return VisioModel(**data)


def load_string(json_string):
    data = json.loads(json_string)
    return VisioModel(**data)


def save_file(json_object: VisioModel, json_path: str):
    with open(json_path, 'w') as f:
        f.write(json_object.model_dump_json(by_alias=True))