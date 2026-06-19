from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact,
)

import os
import sys

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            self.dataingestionconfig = DataIngestionConfig(self.training_pipeline_config)
            dataingestion = DataIngestion(self.dataingestionconfig)
            logging.info("Initiate the data ingestion")
            dataingestionartifact = dataingestion.initiate_data_ingestion()
            logging.info("Data Ingestion Completed")
            return dataingestionartifact
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_data_validation(self,dataingestionartifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            datavalidationconfig = DataValidationConfig(self.training_pipeline_config)
            datavalidation = DataValidation(dataingestionartifact,datavalidationconfig)
            logging.info("Data Validation started")
            data_validation_artifact = datavalidation.initiate_data_validation()
            logging.info("Data Validation Completed")
            return data_validation_artifact            
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact)->DataTransformationArtifact:
        try:
            datatransformationconfig = DataTransformationConfig(self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact,datatransformationconfig)
            logging.info("Data Transformation started")
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data Transformation Completed")
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            modeltrainerconfig = ModelTrainerConfig(self.training_pipeline_config)
            modeltrainer = ModelTrainer(data_transformation_artifact,modeltrainerconfig)
            logging.info("Model Training started")
            model_trainer_artifact = modeltrainer.initiate_model_trainer()
            logging.info("Model Training Completed")
            return model_trainer_artifact            
        except Exception as e:
            raise CustomException(e,sys)
    
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(dataingestionartifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)


    