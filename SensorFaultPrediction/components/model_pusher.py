from SensorFaultPrediction.entity.config_entity import ModelPusherConfig
from SensorFaultPrediction.entity.artifact_entity import ModelPusherArtifact,ModelEvaluatorArtifact
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
import os, sys
import shutil
class ModelPusher:
    def __init__(self,model_pusher_config:ModelPusherConfig,
                 model_evaluation_artifact:ModelEvaluatorArtifact):
        try:
            self.model_pusher_config=model_pusher_config
            self.model_evaluation_artifact=model_evaluation_artifact
        except Exception as e:
            raise MLException(e,sys)
        
    def initiate_model_push(self)->ModelPusherArtifact:
        try:
            trained_model_path = self.model_evaluation_artifact.trained_model_path
            
            #Creating model pusher dir to save model from trained model path
            model_file_path = self.model_pusher_config.model_file_path
            print(model_file_path)
            os.makedirs(os.path.dirname(model_file_path),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=model_file_path)

            #Creating saved model dir to save model from trained model path
            saved_model_path = self.model_pusher_config.saved_model_file_path
            os.makedirs(os.path.dirname(saved_model_path),exist_ok=True)
            shutil.copy(src=trained_model_path, dst=saved_model_path)

            #prepare artifact
            model_pusher_artifact = ModelPusherArtifact(saved_model_file_path=saved_model_path, model_file_path=model_file_path)
            return model_pusher_artifact
        except  Exception as e:
            raise MLException(e, sys)