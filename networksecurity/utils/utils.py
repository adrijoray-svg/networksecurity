import os
import sys
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
import numpy as np 
import pandas as pd
import dill
import pickle
import yaml
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score

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

def save_numpy_array_data(file_path:str, array:np.array)->None:
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok = True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise CustomException(e,sys)
    
def save_object(file_path:str, obj:object)->None:
    try:
        logging.info("Entred the save_object method of Utils Class")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok = True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj,file_obj)
        logging.info("Exited the save_object method of Utils Class")
    except Exception as e:
        raise CustomException(e,sys)

def load_numpy_array_data(file_path:str,):
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)

def load_object(file_path:str):
    try:
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys)

def evaluate_models(x_train,y_train,x_test,y_test,models:dict,params:dict):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            param = params[list(models.keys())[i]]
            
            rs = RandomizedSearchCV(model,param,cv=3)
            rs.fit(x_train,y_train)

            model.set_params(**rs.best_params_)
            model.fit(x_train,y_train)

            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report
    except Exception as e:
        raise CustomException(e,sys)