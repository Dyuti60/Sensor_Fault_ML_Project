from SensorFaultPrediction.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from SensorFaultPrediction.entity.config_entity import DataValidationConfig
from SensorFaultPrediction.constant.training_pipeline import SCHEMA_FILE_PATH
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
from SensorFaultPrediction.utils.mail_utils import read_yaml_file,write_yaml_file
import os, sys
import pandas as pd
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise MLException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame):
        try:
            columns_in_data=list(dataframe.columns.values)
            columns_in_schema=[]
            schema_cols=self._schema_config['columns']
            for value in schema_cols:
                cols=str(list(value.keys())[0])
                columns_in_schema.append(cols)

            missing_columns_in_data=[]
            for columns in columns_in_schema:
                if columns not in columns_in_data:
                    missing_columns_in_data.append(columns)
                    return False
                else:
                    return True
        except Exception as e:
            raise MLException(e,sys)

    def does_numerical_column_exists(self,dataframe:pd.DataFrame):
        try:
            numerical_columns_in_schema=self._schema_config['numerical_columns']
            columns_in_data=list(dataframe.columns.values)
            missing_numerical_columns_in_data=[]
            for columns in numerical_columns_in_schema:
                if columns not in columns_in_data:
                    missing_numerical_columns_in_data.append(columns)
                    return False
                else:
                    return True
        except Exception as e:
            raise MLException(e,sys)
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path,low_memory=False)
        except Exception as e:
            raise MLException(e,sys)
    def detect_dataset_drift(self, base_df, current_df, threshold=0.05):
        try:
            report={}
            validation_status=True
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_same_distribution=ks_2samp(d1,d2)
                if threshold<=is_same_distribution.pvalue:
                    drift_found=False
                    validation_status=True
                else:
                    drift_found=True
                    validation_status=False
                report.update({column:{
                    'drift_found':drift_found,
                    'p_value':float(is_same_distribution.pvalue),
                    'threshold':threshold,
                }})

            drift_report_file_dir=self.data_validation_config.drift_report_file_dir
            drift_report_file_path=self.data_validation_config.drift_report_file_path
            os.makedirs(drift_report_file_dir,exist_ok=True)
            write_yaml_file(drift_report_file_path,report)
            return validation_status
                    
        except Exception as e:
            raise MLException(e,sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            error_message=''
            train_data=self.data_ingestion_artifact.train_file_path
            test_data=self.data_ingestion_artifact.test_file_path

            train_dataframe=self.read_data(train_data)
            test_dataframe=self.read_data(test_data)

            train_status_all_cols=self.validate_number_of_columns(train_dataframe)
            test_status_all_cols=self.validate_number_of_columns(test_dataframe)

            train_status_num_cols=self.does_numerical_column_exists(train_dataframe)
            test_status_num_cols=self.does_numerical_column_exists(test_dataframe)

            validate_num_of_columns_status=[]
            validate_num_of_columns_status.append(train_status_all_cols)
            validate_num_of_columns_status.append(test_status_all_cols)

            validate_all_num_columns_status=[]
            validate_all_num_columns_status.append(train_status_num_cols)
            validate_all_num_columns_status.append(test_status_num_cols)

            if 'False' in validate_num_of_columns_status:
                error_message='Number of columns in dataframe doesnot contain all columns mentioned in schema'

                if 'False' in validate_all_num_columns_status:
                    error_message='Number of numerical columns in dataframe doesnot contain all numerical columns mentioned in schema'
                    invalid_dir=self.data_validation_config.invalid_data_dir
                    os.makedirs(invalid_dir, exist_ok=True)
                    train_file_path=self.data_validation_config.invalid_train_file_path
                    test_file_path=self.data_validation_config.invalid_test_file_path
            else:
                invalid_dir=self.data_validation_config.valid_data_dir
                os.makedirs(invalid_dir, exist_ok=True)
                train_file_path=self.data_validation_config.valid_train_file_path
                test_file_path=self.data_validation_config.valid_test_file_path
            
            train_dataframe.to_csv(train_file_path,index=False,header=True)
            test_dataframe.to_csv(test_file_path,index=False,header=True)

            if len(error_message)>0:
                raise Exception(error_message)
            
            validation_status=self.detect_dataset_drift(train_dataframe,test_dataframe)
            data_validation_artifacts=DataValidationArtifact(validation_status=validation_status,
                                                             valid_train_file_path=self.data_validation_config.valid_train_file_path,
                                                             valid_test_file_path=self.data_validation_config.valid_test_file_path,
                                                             invalid_test_file_path=self.data_validation_config.invalid_train_file_path,
                                                             invalid_train_file_path=self.data_validation_config.invalid_test_file_path,
                                                             drift_report_file_path=self.data_validation_config.drift_report_file_path)
            return data_validation_artifacts
        except Exception as e:
            raise MLException(e,sys)
