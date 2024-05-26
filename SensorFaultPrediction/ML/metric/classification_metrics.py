from SensorFaultPrediction.entity.artifact_entity import ClassificationMetricArtifact
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
import os, sys
from sklearn.metrics import f1_score, precision_score, recall_score

def get_classification_score(actual, pred):
    try:
        model_f1_score=f1_score(actual, pred)
        model_precision_score=precision_score(actual, pred)
        model_recall_score=recall_score(actual, pred)
        classfication_artifacts=ClassificationMetricArtifact(model_f1_score,model_precision_score,model_recall_score)
        return classfication_artifacts
    except Exception as e:
        raise MLException(e,sys)