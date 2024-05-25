from SensorFaultPrediction.entity.config_entity import ModelTrainingConfig
from SensorFaultPrediction.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
from SensorFaultPrediction.utils.mail_utils import load_numpy_array_data
from SensorFaultPrediction.utils.mail_utils import load_object
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
import os, sys

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainingConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise MLException(e,sys)
        
    
    def perform_hyperparameter_tuning(self):
        pass

    def train_model(self):
        pass

    def initiate_model_training(self)-> ModelTrainerArtifact:
        pass

    

