from SensorFaultPrediction.pipeline.training_pipeline import TrainingPipeline
from SensorFaultPrediction.entity.config_entity import TrainingPipelineConfig
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
import os, sys

if __name__ == '__main__':
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.run_train_pipeline()
    except Exception as e:
        raise MLException(e,sys)
