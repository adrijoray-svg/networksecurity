import os
import sys
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
import numpy as np 
import pandas as pd
import dill
import pickle
import yaml

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path,"rb") as fileobj:
            return yaml.safe_load(fileobj)
    except Exception as e:
        raise CustomException(e,sys)

def write_yaml_file(file_path:str, content:object, replace:bool = False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok = True)
        with open(file_path,"w") as file:
            yaml.dump(content,file)
    except Exception as e:
        raise CustomException(e,sys)