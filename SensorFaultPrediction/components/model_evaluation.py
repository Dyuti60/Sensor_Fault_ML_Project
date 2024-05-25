from SensorFaultPrediction.entity.config_entity import ModelEvaluationConfig
from SensorFaultPrediction.entity.artifact_entity import ModelEvaluatorArtifact, ModelTrainerArtifact,DataValidationArtifact
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
import os, sys
import pandas as pd

class ModelEvaluation:
    def __init__(self,model_trainer_artifact:ModelTrainerArtifact,
                 model_evaluation_config:ModelEvaluationConfig,
                 data_validation_artifact:DataValidationArtifact):
        try:
            self.model_trainer_artifact=model_trainer_artifact
            self.model_evaluation_config=model_evaluation_config
            self.data_validation_artifact=data_validation_artifact
        except Exception as e:
            raise MLException(e,sys)
        
    def initiate_model_evaluation(self)->ModelEvaluatorArtifact:
        pass
