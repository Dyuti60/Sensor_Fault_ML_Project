from SensorFaultPrediction.entity.config_entity import ModelPusherConfig
from SensorFaultPrediction.entity.artifact_entity import ModelPusherArtifact,ModelEvaluatorArtifact
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
import os, sys
class ModelPusher:
    def __init__(self,model_pusher_config:ModelPusherConfig,
                 model_evaluation_artifact:ModelEvaluatorArtifact):
        try:
            self.model_pusher_config=model_pusher_config
            self.model_evaluation_artifact=model_evaluation_artifact
        except Exception as e:
            raise MLException(e,sys)
        
    def initiate_model_push(self)->ModelPusherArtifact:
        pass