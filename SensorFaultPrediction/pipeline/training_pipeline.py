from SensorFaultPrediction.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from SensorFaultPrediction.entity.artifact_entity import DataIngestionArtifact
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
from SensorFaultPrediction.components.data_ingestion import DataIngestion
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
        
    def run_train_pipeline(self):
        try:
            data_ingestion_artifact:DataIngestionArtifact = self.start_data_ingestion()
        except Exception as e:
            raise MLException(e,sys)