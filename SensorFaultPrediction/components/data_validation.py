from SensorFaultPrediction.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from SensorFaultPrediction.entity.config_entity import DataValidationConfig
from SensorFaultPrediction.constant.training_pipeline import SCHEMA_FILE_PATH
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
from SensorFaultPrediction.utils.mail_utils import read_yaml_file,write_yaml_file
import os, sys
import pandas as pd

class DataValidation:
    def __init__(self,data_ingestion_artifact=DataIngestionArtifact,
                 data_validation_config=DataValidationConfig):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise MLException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame):
        pass

    def does_numerical_column_exists(self,dataframe:pd.DataFrame):
        pass

    def read_data(file_path)->pd.DataFrame:
        pass

    def detect_dataset_drift(self, base_df, current_df, threshold=0.05):
        pass

    def initiate_data_validation(self)->DataValidationArtifact:
        pass
