from SensorFaultPrediction.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig,DataValidationConfig,DataTransformationConfig
from SensorFaultPrediction.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
from SensorFaultPrediction.components.data_ingestion import DataIngestion
from SensorFaultPrediction.components.data_validation import DataValidation
from SensorFaultPrediction.components.data_transformation import DataTransformation
import os, sys

class TrainingPipeline:
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
        
    def run_train_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
            data_validation_artifact:DataValidationArtifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact:DataTransformationArtifact = self.start_data_transformation(data_validation_artifact)
        except Exception as e:
            raise MLException(e,sys)