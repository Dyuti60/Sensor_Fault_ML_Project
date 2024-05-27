from SensorFaultPrediction.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainingConfig,ModelEvaluationConfig,ModelPusherConfig
from SensorFaultPrediction.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact,ModelEvaluatorArtifact,ModelPusherArtifact
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
from SensorFaultPrediction.components.data_ingestion import DataIngestion
from SensorFaultPrediction.components.data_validation import DataValidation
from SensorFaultPrediction.components.data_transformation import DataTransformation
from SensorFaultPrediction.components.model_trainer import ModelTrainer
from SensorFaultPrediction.components.model_evaluation import ModelEvaluation
from SensorFaultPrediction.components.model_pusher import ModelPusher
from SensorFaultPrediction.cloud_storage.s3_syncer import S3Syncer
from SensorFaultPrediction.constant.training_pipeline import SAVED_MODEL_DIR
from SensorFaultPrediction.constant.s3_bucket import TRAINING_BUCKET_NAME,PREDICTION_BUCKET_NAME
import os, sys

class TrainingPipeline:
    is_pipeline_running=False
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except MLException as e:
            raise MLException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            self.data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=self.data_validation_config)
            data_validation_artifact=data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise MLException(e,sys)
        
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_tranformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=self.data_tranformation_config)
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise MLException(e,sys)
        
    def start_model_training(self,data_transformation_artfact:DataTransformationArtifact):
        try:
            self.model_trainer_config=ModelTrainingConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer=ModelTrainer(model_trainer_config=self.model_trainer_config,data_transformation_artifact=data_transformation_artfact)
            model_trainer_artifact=model_trainer.initiate_model_training()
            return model_trainer_artifact
        except Exception as e:
            raise MLException(e,sys)
        
    def start_model_evaluation(self,model_trainer_artifact:ModelTrainerArtifact,data_validation_artifact:DataValidationArtifact):
        self.model_evaluation_config=ModelEvaluationConfig(training_pipeline_config=self.training_pipeline_config)
        
        model_evaluation=ModelEvaluation(model_trainer_artifact=model_trainer_artifact,
                                         model_eval_config=self.model_evaluation_config,
                                         data_validation_artifact=data_validation_artifact)
        model_evaluation_artifact=model_evaluation.initiate_model_evaluation()
        return model_evaluation_artifact
        
    def start_model_pusher(self,model_eval_artifact:ModelEvaluatorArtifact):
        try:
            model_pusher_config = ModelPusherConfig(training_pipeline_config=self.training_pipeline_config)
            model_pusher = ModelPusher(model_pusher_config, model_eval_artifact)
            model_pusher_artifact = model_pusher.initiate_model_push()
            return model_pusher_artifact
        except  Exception as e:
            raise  MLException(e,sys)

    def sync_artifact_dir_to_s3(self):
        try:
            aws_key_url=f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            folder=self.training_pipeline_config.artifact_dir_name
            S3Syncer.load_to_s3(aws_key_url,folder)
        except Exception as e:
            raise MLException(e,sys)

    def sync_saved_model_dir_to_s3(self):
        try:
            aws_key_url=f"s3://{TRAINING_BUCKET_NAME}/saved_model/{SAVED_MODEL_DIR}"
            folder=SAVED_MODEL_DIR
            S3Syncer.load_to_s3(aws_key_url,folder)
        except Exception as e:
            raise MLException(e,sys)


    def run_train_pipeline(self):
        try:
            TrainingPipeline.is_pipeline_running=True
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact:DataValidationArtifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact:DataTransformationArtifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact:ModelTrainerArtifact=self.start_model_training(data_transformation_artifact)
            model_evaluation_artifact:ModelEvaluatorArtifact=self.start_model_evaluation(model_trainer_artifact,data_validation_artifact)
            #if not model_evaluation_artifact.is_model_accepted:
            #    raise Exception("Trained model is not better than the best model")
            model_pusher_artifact:ModelPusherArtifact=self.start_model_pusher(model_evaluation_artifact)
            TrainingPipeline.is_pipeline_running=False
        except Exception as e:
            TrainingPipeline.is_pipeline_running=False
            raise MLException(e,sys)
        