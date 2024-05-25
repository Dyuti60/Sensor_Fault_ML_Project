import os,sys
import pandas as pd
import numpy as np
from SensorFaultPrediction.entity.config_entity import DataTransformationConfig
from SensorFaultPrediction.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
from SensorFaultPrediction.constant.training_pipeline import TARGET_COLUMN
from SensorFaultPrediction.ml.model.estimator import TargetValueMapping
from SensorFaultPrediction.utils.mail_utils import save_numpy_array_data, save_object

from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline

class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact, 
                    data_transformation_config: DataTransformationConfig,):
        """

        :param data_validation_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: configuration for data transformation
        """
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise MLException(e, sys)
    @staticmethod    
    def read_data(file_path:str):
        return pd.read_csv(file_path)
    @classmethod
    def get_data_transformer_object(cls):
        try:
            robust_Scaler=RobustScaler()
            simple_Imputer=SimpleImputer(strategy='constant',fill_value=0)
            preprocessor=Pipeline(
                steps=[
                    ('simpleImputer',simple_Imputer),
                    ('robustScaler',robust_Scaler)
                ]
            )
            return preprocessor
        except Exception as e:
            raise MLException(e,sys)

    def initiate_data_transformation(self)-> DataTransformationArtifact:
        try:
            train_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            test_df=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            preprocessor=self.get_data_transformer_object()

            #training Dataset
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]

            #test Dataset
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN]

            #TRASNFORMATION
            # 1. Target Column Mapping:
            transformed_target_feature_train_df=target_feature_train_df.replace(TargetValueMapping().to_dict())
            transformed_target_feature_test_df=target_feature_test_df.replace(TargetValueMapping().to_dict())

            # 2. Input feature transformation:
            preprocessor_obj=preprocessor.fit(input_feature_train_df)
            transformed_input_feature_train_df=preprocessor_obj.transform(input_feature_train_df)
            transformed_input_feature_test_df=preprocessor_obj.transform(input_feature_test_df)

            smt=SMOTETomek(sampling_strategy='auto')
            final_input_feature_train_df,final_target_feature_train_df=smt.fit_resample(transformed_input_feature_train_df,transformed_target_feature_train_df)
            final_input_feature_test_df,final_target_feature_test_df=smt.fit_resample(transformed_input_feature_test_df,transformed_target_feature_test_df)

            train_arr=np.c_[final_input_feature_train_df,np.array(final_target_feature_train_df)]
            test_arr=np.c_[final_input_feature_test_df,np.array(final_target_feature_test_df)]
            print(type(train_arr))
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_obj)

            data_transformation_artifacts=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifacts
        except Exception as e:
            raise MLException(e,sys)

