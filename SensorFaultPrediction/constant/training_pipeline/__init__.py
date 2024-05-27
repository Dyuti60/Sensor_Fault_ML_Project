import os

#Training Pipeline:
MODEL_TRAINING_PIPELINE_NAME='training_pipeline'
ARTIFACT_DIR:str='artifact'

#Model Evaluation Save model
SAVED_MODEL_DIR =os.path.join("SAVED_MODEL")



#Data Ingestion Constants
DATA_INGESTION_DIR_NAME:str='data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR:str='feature_store'
FILE_NAME:str='sensor.csv'
DATA_INGESTION_DIR:str='ingested'
TRAIN_FILE_NAME:str='train.csv'
TEST_FILE_NAME:str='test.csv'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float=0.2
DATA_INGESTION_COLLECTION_NAME:str='Attendance_Sensor_Data'
SCHEMA_FILE_PATH=os.path.join('config','schema.yaml')
SCHEMA_DROP_COLUMNS='drop_columns'

TARGET_COLUMN:str='class'

#Data Validation Constants
DATA_VALIDATION_DIR='data_validation'
DATA_VALIDATION_VALID_DIR : str ='valid'
DATA_VALIDATION_INVALID_DIR: str ='invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str ='drift_report.yaml'

#Data Transformation Constants
DATA_TRANSFORMATION_DIR:str='data_transformation'
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = 'transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = 'transformed_object'
PREPROCESSING_OBJECT_FILE_PATH='preprocessing.pkl'

#Model Training Constants
MODEL_TRAINED_DIR:str = 'model_trained'
MODEL_TRAINING_REPORT_DIR:str='model_training_metrics'
MODEL_TRAINING_REPORT_FILE_NAME:str='model_training_metrics_report.csv'
MODEL_TRAINER_TRAINED_MODEL_DIR:str = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_NAME: str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD: float = 0.05

#Model Evaluation Constants
MODEL_EVALUATION_DIR='model_evaluation'
MODEL_EVALUATION_CHANGED_THRESHOLD: float = 0.02
MODEL_EVALUATION_REPORT_NAME: str = "report.yaml"

#Model Pusher Constants
MODEL_PUSHER_DIR='model_pusher'
MODEL_PUSHER_SAVED_MODEL_DIR: str ='SAVED_MODEL'

