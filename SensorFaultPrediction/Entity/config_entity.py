from datetime import datetime
import os
from SensorFaultPrediction.constant import training_pipeline

class TrainingPipelineConfig:
    '''
    when creating object of TrainingPipelineConfig, pass parameters like current timestamp to initialize 'pipeline name',
    'timestamp' and 'artifact directory path'
    '''
    def __init__(self,current_timestamp=datetime.now()):
        timestamp=current_timestamp.strftime('%m_%d_%Y_%H_%M_%S')
        self.pipeline_dir_name:str=training_pipeline.MODEL_TRAINING_PIPELINE_NAME
        self.artifact_dir_name:str=os.path.join(training_pipeline.ARTIFACT_DIR,timestamp)
        self.timestamp:str=timestamp

class DataIngestionConfig:
    '''
    when creating object of DataIngestionConfig, initialises 'data_ingestion_directory',
    'feature store file path', 'training file path', 'testing file path', 'train_test_split_ratio' and 'collection name'

    artifact/data_ingestion
    artifact/data_ingestion/feature_store/sensor.csv
    artifact/data_ingestion/ingested/train.csv
    artifact/data_ingestion/ingested/test.csv
    '''
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir=os.path.join(training_pipeline_config.artifact_dir_name,training_pipeline.DATA_INGESTION_DIR_NAME)
        self.feature_store_file_path=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,training_pipeline.FILE_NAME)
        self.training_file_path=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_DIR,training_pipeline.TRAIN_FILE_NAME)
        self.testing_file_path=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_DIR,training_pipeline.TEST_FILE_NAME)
        self.train_test_split_ratio=training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name=training_pipeline.DATA_INGESTION_COLLECTION_NAME

class DataValidationConfig:
    '''
    when creating object of DataValidationConfig, initialises 'validation directory',
    'valid data directory', 'invalid data directory', 'valid train file path', 'invalid train file path'. 'valid test file path',
    'invalid test file path', 'drift report file path'

    artifact/data_validation/
    artifact/data_validation/valid_data
    artifact/data_validation/valid_data/train.csv
    artifact/data_validation/valid_data/test.csv
    artifact/data_validation/invalid_data
    artifact/data_validation/invalid_data/train.csv
    artifact/data_validation/invalid_data/test.csv
    artifact/data_validation/driftreport/drift_repot.yaml
    '''
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir:str = os.path.join(training_pipeline_config.artifact_dir_name,training_pipeline.DATA_VALIDATION_DIR)
        self.valid_data_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.valid_train_file_path:str=os.path.join(self.valid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path:str=os.path.join(self.valid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.invalid_data_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.invalid_train_file_path:str=os.path.join(self.invalid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path:str=os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_dir:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR)
        self.drift_report_file_path:str=os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

class DataTransformationConfig:
    '''
    when creating object of DataTransformationConfig, initialises 'transform directory', 'transformed train file path', 
    'transformed test file path' and 'transformed object file path'
    
    artifact/data_transformation/
    artifact/data_transformation/transformed_data/train.npy
    artifact/data_transformation/transformed_data/test.npy
    artifact/data_transformation/transformed_object/preprocessing.pkl
    '''
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir:str=os.path.join(training_pipeline_config.artifact_dir_name,training_pipeline.DATA_TRANSFORMATION_DIR)
        self.transformed_train_file_path:str=os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,training_pipeline.TRAIN_FILE_NAME.replace('csv','npy'))
        self.transformed_test_file_path:str=os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,training_pipeline.TEST_FILE_NAME.replace('csv','npy'))
        self.transformed_object_file_path:str=os.path.join(self.data_transformation_dir,training_pipeline.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,training_pipeline.PREPROCESSING_OBJECT_FILE_PATH)

class ModelTrainingConfig:
    '''
    when creating object of ModelTrainingConfig, initialises 'model trainer directory', 'modelled object directory',
    'expected accuracy' and 'overfitting underfitting threshold'
    
    artifact/model_trained/
    artifact/model_trainer/model.pkl
    '''
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_trained_dir=os.path.join(training_pipeline_config.artifact_dir_name,training_pipeline.MODEL_TRAINED_DIR)
        self.model_training_report_dir=os.path.join(self.model_trained_dir,training_pipeline.MODEL_TRAINING_REPORT_DIR)
        self.model_training_report_file_path=os.path.join(self.model_training_report_dir,training_pipeline.MODEL_TRAINING_REPORT_FILE_NAME)
        self.model_trained_object_file_path=os.path.join(self.model_trained_dir,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_DIR,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)
        self.expected_accuracy:float=training_pipeline.MODEL_TRAINER_EXPECTED_SCORE
        self.overfitting_underfitting_threshold:float=training_pipeline.MODEL_TRAINER_OVERFITTING_UNDERFITTING_THRESHOLD

class ModelEvaluationConfig:
    '''
    when creating object of ModelEvaluationConfig, initialises 'model evaluation dir', 'report file', 'change threshold'
    
    artifact/model_evaluation/
    artifact/model_evaluation/report.yaml
    '''

class ModelEvaluationConfig:

    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_evaluation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir_name, training_pipeline.MODEL_EVALUATION_DIR
        )
        self.report_file_path = os.path.join(self.model_evaluation_dir,training_pipeline.MODEL_EVALUATION_REPORT_NAME)
        self.change_threshold = training_pipeline.MODEL_EVALUATION_CHANGED_THRESHOLD



class ModelPusherConfig:
    '''
    when creating object of ModelPusherConfig, initialises 'saved model path' and 'trained model path'
    
    artifact/model_pusher/
    artifact/model_pusher/model.pkl
    SAVED_MODEL/{timestamp}/model.pkl
    '''
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.model_pusher_dir=os.path.join(training_pipeline_config.artifact_dir_name,training_pipeline.MODEL_PUSHER_DIR)
        self.model_file_path=os.path.join(self.model_pusher_dir,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)
        self.saved_model_file_path=os.path.join(training_pipeline.MODEL_PUSHER_SAVED_MODEL_DIR,training_pipeline.MODEL_TRAINER_TRAINED_MODEL_NAME)
        
