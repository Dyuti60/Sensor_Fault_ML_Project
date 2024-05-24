from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
from SensorFaultPrediction.entity.config_entity import TrainingPipelineConfig
from SensorFaultPrediction.entity.config_entity import DataIngestionConfig
from SensorFaultPrediction.entity.artifact_entity import DataIngestionArtifact
from SensorFaultPrediction.data_source_access.sensor_data import AttendanceSensorData
from sklearn.model_selection import train_test_split
import os, sys
import pandas as pd

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise MLException(e,sys)

    def export_data_into_feature_store(self):
        try:
            Attendance_Sensor_Data=AttendanceSensorData()
            dataframe=Attendance_Sensor_Data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise MLException(e,sys)
        
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,self.data_ingestion_config.train_test_split_ratio)
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
        except Exception as e:
            return MLException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_data_into_feature_store()
            #dataframe.drop[columns=self._schema_config['drop_columns'],axis=1]
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifacts=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                           test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifacts
        except Exception as e:
            raise MLException(e,sys)



