from dataclasses import dataclass

'''
Artifacts are the outputs received at various stages of the ML Project:
In this project, we will receive artifacts at 7 stages:
1. Data Ingestion
2. Data Validation
3. Data Transformation
4. Classification Metrics Output
5. Model Trainer
6. Model Evaluation
7. Model Pusher
'''

@dataclass
class DataIngestionArtifact:
    '''
    In Data Ingestion, we will receive data from feature store : 
    Mongo db and then split into train and test data files, which will be stored in filepaths
    These train and test file paths will be the output of data ingestion phase
    '''
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifact:
    '''
    In Data Validation, we will validate the train and test data files received from data ingestion phase and check for column counts,
    numerical columns and there by tell the validation status, generate drift report, invalid and valid train and test files.
    These valid and invalid train and test file paths,drift report and validation status will be the output of data validation phase.
    '''
    validation_status:bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str

@dataclass
class DataTransformationArtifact:
    '''
    In Data Transformation, we will transform the train and test data files received from data validation phase based on preprocessor
    These transformed train and test and preprocessor objects file paths will be the output of data transformation phase.
    '''
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str


@dataclass
class ClassificationMetricArtifact:
    '''
    Classification Metrics helps calculate f1 score, precision score, recall score between the actual and predicted output of the model
    These f1 score, precision score, recall score will be the output of classification metrics phase.
    '''
    f1_score:float
    precision_score:float
    recall_score:float

@dataclass
class ModelTrainerArtifact:
    '''
    In Model Training phase, Model is being trained by the training dataset, the output of this stage are the model file path,
    training metrics and testing metrics.
    '''
    trained_model_file_path:str
    train_metrics_artifact: ClassificationMetricArtifact
    test_metrics_artifact: ClassificationMetricArtifact

@dataclass
class ModelEvaluatorArtifact:
    '''
    In this stage, model is trained and evaluated on different variances
    Output are: is_model_accepted, improved_accuracy, best_model_path, trained_model_path, train_model_metric, best_model_metric
    '''
    is_model_accepted: bool
    improved_accuracy: float
    best_model_path: str
    trained_model_path: str
    train_model_metric_artifact: ClassificationMetricArtifact
    best_model_metric_artifact: ClassificationMetricArtifact

@dataclass
class ModelPusherArtifact:
    '''
    The model is saved for future reference, its being copied from model file path to saved model file path
    '''
    model_file_path:str
    saved_model_file_path:str