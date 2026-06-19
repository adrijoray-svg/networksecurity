import os
import sys
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig

from networksecurity.utils.utils import save_numpy_array_data,save_object,load_numpy_array_data,load_object,evaluate_models
from networksecurity.utils.ml_utils.metric import get_classification_score
from networksecurity.utils.ml_utils.model import NetworkModel

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier

import numpy as np
import pandas as pd
import mlflow
import dagshub
dagshub.init(repo_owner='adrijoray-svg', repo_name='networksecurity', mlflow=True)

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelTrainerArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def track_mlflow(self,best_model,classification_metric):
        with mlflow.start_run():
            f1 = classification_metric.f1_score
            precision = classification_metric.precision_score
            recall = classification_metric.recall_score

            mlflow.log_metric("f1_score",f1)
            mlflow.log_metric("precision",precision)
            mlflow.log_metric("recall",recall)
            mlflow.sklearn.log_model(best_model,"model")
        
    def train_model(self,x_train,y_train,x_test,y_test):
        models = {
            'LogisticRegression':LogisticRegression(),
            'DecisionTree':DecisionTreeClassifier(),
            'RandomForest':RandomForestClassifier(),
            'AdaBoost':AdaBoostClassifier(),
            'GradientBoost':GradientBoostingClassifier()
        }
        params={
            "DecisionTree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "RandomForest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "GradientBoost":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "LogisticRegression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
        }
        model_report: dict = evaluate_models(x_train,y_train,x_test,y_test,models,params)

        best_model_score = max(sorted(model_report.values()))
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]
        y_train_pred = best_model.predict(x_train)
        classification_train_metric = get_classification_score(y_train,y_train_pred)
        self.track_mlflow(best_model,classification_train_metric)

        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(y_test,y_test_pred)
        self.track_mlflow(best_model,classification_test_metric)

        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        os.makedirs(os.path.dirname(self.model_trainer_config.trained_model_file_path))

        network_model=NetworkModel(preprocessor,model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path,network_model) 
        save_object("final_model/model.pkl",best_model)

        model_trainer_artifact = ModelTrainerArtifact(
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric,
            trained_model_file_path=self.model_trainer_config.trained_model_file_path
        )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact
    

    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)

            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            model_trainer_artifact = self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
