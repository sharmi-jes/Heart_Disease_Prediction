import os
import sys
import yaml
import numpy as np
import pickle
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
    
def save_object(file_path,obj:object):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as f:
            pickle.dump(obj,f)
    except Exception as e:
        raise HeartDiasesException(e,sys)

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise HeartDiasesException(e, sys) from e