from networksecurity.entity.artifact_entity import ClassificationMetric
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging
from sklearn.metrics import f1_score,precision_score,recall_score
import os
import sys

def get_classification_score(y_true,y_pred)->ClassificationMetric:
    try:
        f1 = f1_score(y_true,y_pred)
        precision = precision_score(y_true,y_pred)
        recall = recall_score(y_true,y_pred)

        classification_metric = ClassificationMetric(f1_score=f1,
                                                     precision_score=precision,
                                                     recall_score=recall)
        return classification_metric
    except Exception as e:
        raise CustomException(e,sys)