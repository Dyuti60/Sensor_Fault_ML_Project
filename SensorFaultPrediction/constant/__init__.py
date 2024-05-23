import os


#Data Ingestion Constants
DATA_INGESTION_COLLECTION_NAME:str='Attendance_Sensor_Data'
DATA_INGESTION_DIR_NAME:str='data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR:str='feature_store'
DATA_INGESTION_INGESTED_DIR:str='ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float=0.2

TARGET_COLUMN:str='class'
TRAIN_FILE_NAME:str='train.csv'
TEST_FILE_NAME:str='test.csv'
ARTIFACT_DIR:str='artifact'
FILE_NAME:str='sensor.csv'

schema_file_path=os.path.join('config','schema.yaml')
schema_drop_cols='drop_columns'

#Data Validation Constants
DATA_VALIDATION_VALID_DIR : str ='valid'
DATA_VALIDATION_INVALID_DIR: str ='invalid'
DATA_VALIDATION_DRIFT_REPORT_DIR: str = 'drift_report'
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str ='drift_report.yaml'

#Data Transformation Constants
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = 'transformed'
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = 'transformed_object'
PREPROCESSING_OBJECT_FILE_PATH='preprocessing.pkl'

#Model Training Constants
MODEL_TRAINER_TRAINED_MODEL_DIR:str = 'model_trainer'
MODEL_TRAINER_TRAINED_MODEL_NAME: str = 'model.pkl'
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD: float = 0.05

#Model Evaluation Constants
MODEL_EVALUATION_CHANGED_THRESHOLD: float = 0.02
MODEL_EVALUATION_REPORT_NAME: str = "report_yaml"

#Model Pusher Constants
MODEL_PUSHER_SAVED_MODEL_DIR: str ='SAVED_MODEL'

