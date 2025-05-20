import os
import sys
import yaml
from Heart_Disease_Prediction.exception.exception import HeartDiasesException


def read_yaml_file(file_path):
    try:
        with open(file_path,"r") as f:
            yaml.safe_load(f)
    except Exception as e:
        raise HeartDiasesException(e,sys)


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise HeartDiasesException(e, sys)
