from SensorFaultPrediction.entity.config_entity import ModelTrainingConfig
from SensorFaultPrediction.entity.artifact_entity import ModelTrainerArtifact, DataTransformationArtifact
from SensorFaultPrediction.utils.mail_utils import load_numpy_array_data,load_object
from SensorFaultPrediction.ml.metric.classification_metrics import get_classification_score
from SensorFaultPrediction.ml.model.estimator import SensorModel
from SensorFaultPrediction.utils.mail_utils import save_object
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import GridSearchCV

import pandas as pd


import os, sys

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainingConfig,data_transformation_artifact:DataTransformationArtifact):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise MLException(e,sys)
        
    
    def models_dict(self):
        models={
            #'Logistic Regression':LogisticRegression(),
            #'SVC':SVC(),
            #'KNN Classifier':KNeighborsClassifier(),
            #'Decision Tree Classifier':DecisionTreeClassifier(),
            #'Random Forest Classifier':RandomForestClassifier(),
            #'Gradient Boosting Classifier':GradientBoostingClassifier(),
            #'Ada Boost Classifier':AdaBoostClassifier(),
            'XGBoost Classifier':XGBClassifier(),
            #'CatBoost Classifier':CatBoostClassifier()
        }
        return models

    def hyperparameterTuning_Params_Actual(self):
        params={
            'Logistic Regression':{
                #'penalty':['l1', 'l2', 'elasticnet', None],
                #'C':[1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0],
                'max_iter':[50000],
                'solver':['liblinear','lbfgs']
                #'solver':['lbfgs', 'liblinear', 'newton-cg', 'newton-cholesky', 'sag', 'saga']
                #'l1_ratio':[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
            },
            'SVC':{
                'kernel':['linear', 'poly', 'rbf', 'sigmoid'],
                'C':[1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0],
                #'coef0':[0.1,0.2,0.5,0.8,1.0,1.2] 
            },
            'KNN Classifier':{
                'n_neighbors':[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
            },
            'Decision Tree Classifier':{
                'criterion':['gini', 'entropy', 'log_loss'],
                'splitter':['best', 'random'],
                'ccp_alpha':[1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0],
                'max_features':['sqrt','log2']
            },
            'Random Forest Classifier':{
                'criterion':['gini', 'entropy', 'log_loss'],
                'n_estimators':[2,4,9,16,25,36,49,64,81,100],
                'max_features':['sqrt','log2'],
                'ccp_alpha':[1.0,1.5,2.0,2.5,3.0,3.5,4.0,4.5,5.0],
            },
            'Gradient Boosting Classifier':{
                'loss':['exponential','log_loss'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                'max_features':['sqrt','log2'],
                'n_estimators':[2,4,9,16,25,36,49,64,81,100],
            },
            'XGBoost Classifier':{
                'learning_rate':[.1,.01,.05,.001],
                'n_estimators': [2,4,9,16,25,36,49,64,81,100]
            },

            "CatBoost Classifier":{
                'depth': [6,8,10],
                'learning_rate': [0.01, 0.05, 0.1],
                #'iterations': [30, 50, 100]
            },
            "Ada Boost Classifier":{
                'learning_rate':[.1,.01,0.5,.001],
                # 'loss':['linear','square','exponential'],
                'n_estimators': [2,4,9,16,25,36,49,64,81,100]
            }
        }
        return params

    def hyperparameterTuning_Params(self):
        params={
            'Logistic Regression':{},
            'SVC':{},
            'KNN Classifier':{},
            'Decision Tree Classifier':{},
            'Random Forest Classifier':{},
            'Gradient Boosting Classifier':{},
            'XGBoost Classifier':{
                'learning_rate':[.1,.01,.05,.001],
                'n_estimators': [2,4,9,16,25,36,49,64,81,100]
            },
            "CatBoost Classifier":{},
            "Ada Boost Classifier":{}
        }
        return params


    def perform_hyperparameter_tuning(self,model,params):
        hypertuned_model=GridSearchCV(model,params,cv=5)
        return hypertuned_model
        

    def train_model(self,X_train,X_test,y_train,y_test):
        try:
            model_dicts=self.models_dict()
            hyperparameters=self.hyperparameterTuning_Params()
            best_param_model_list=[]
            model_score_test_list=[]
            model_score_train_list=[]
            model_name_list=[]
            model_score_var_list=[]
            for i in range(len(model_dicts)):
                model_name=str(list(model_dicts.keys())[i])
                print(model_name)
                model=list(model_dicts.values())[i]
                hyperparameter=hyperparameters[model_name]
                logging.info("model_name {}, model {}, hyperparameter{}".format(model_name,model,hyperparameter))
                hypertuned_model=self.perform_hyperparameter_tuning(model, hyperparameter)
                hypertuned_model.fit(X_train, y_train)
                y_train_pred=hypertuned_model.predict(X_train)
                y_test_pred=hypertuned_model.predict(X_test)
                logging.info('done with prediction')
                #training score:
                classification_train_metrics =get_classification_score(y_train, y_train_pred)
                #testing score:
                classification_test_metrics =get_classification_score(y_test, y_test_pred)
                logging.info('done with classification metrics {}'.format(classification_test_metrics))
                logging.info('done with classification metrics {}'.format(classification_train_metrics))
                model_name_list.append(model_name)
                best_param_model_list.append(hypertuned_model.best_params_)
                model_score_test_list.append(classification_train_metrics.f1_score)
                model_score_train_list.append(classification_test_metrics.f1_score)
                model_score_var_list.append(abs(classification_test_metrics.f1_score-classification_train_metrics.f1_score))

            report_model=pd.DataFrame(list(zip(model_name_list,best_param_model_list,model_score_test_list,model_score_train_list,model_score_var_list)),
                                      columns=['Model Name','Model Best Parameter',
                                               'Model Score Test','Model Score Train',
                                               'Model Score Variance']).sort_values(by=['Model Score Test','Model Score Variance'],ascending=[False,True])
            report_model=report_model[report_model['Model Score Variance']<self.model_trainer_config.overfitting_underfitting_threshold]
            report_model.reset_index(drop=True)
            logging.info('metrics report generated')
            model_trained_dir=os.path.dirname(self.model_trainer_config.model_trained_dir)
            os.makedirs(model_trained_dir,exist_ok=True)
            model_training_file_dir=self.model_trainer_config.model_training_report_dir
            os.makedirs(model_training_file_dir,exist_ok=True)
            model_training_report_file_path=self.model_trainer_config.model_training_report_file_path
            
            report_model.to_csv(model_training_report_file_path,index=False,header=True)
            return hypertuned_model,report_model,classification_train_metrics,classification_test_metrics
        except Exception as e:
            raise MLException(e,sys)

    def initiate_model_training(self)-> ModelTrainerArtifact:
        try:
            train_array=load_numpy_array_data(self.data_transformation_artifact.transformed_train_file_path)
            test_array=load_numpy_array_data(self.data_transformation_artifact.transformed_test_file_path)
            logging.info('dataset splitted into train and test independent and target features dataset')
            X_train, X_test, y_train, y_test=train_array[:,:-1],test_array[:,:-1],train_array[:,-1],test_array[:,-1]
            hypertuned_model,report_model,classification_train_metrics,classification_test_metrics=self.train_model(X_train, X_test, y_train, y_test)
            
            if len(report_model['Model Name'])==0:
                raise "Model is overfilling or underfitting could not cross the threshold limit"
            '''
            best_model_name=str(report_model['Model Name'][0])
            model_dict=self.models_dict()
            best_model=model_dict[best_model_name]
            best_model_parameter=str(report_model['Model Best Parameter'][0])
            hypertuned_model=self.perform_hyperparameter_tuning(best_model,best_model_parameter)
            '''
            y_test_pred=hypertuned_model.predict(X_test)

            preprocessor=load_object(self.data_transformation_artifact.transformed_object_file_path)
            logging.info('preprocessor object loaded')
            
            #trained_model_dir=os.path.dirname(self.model_trainer_config.model_trained_dir)
            #os.makedirs(model_dir,exist_ok=True)
            model_file_path=self.model_trainer_config.model_trained_object_file_path

            sensor_model=SensorModel(preprocessor=preprocessor,model=hypertuned_model)
            save_object(file_path=model_file_path,
                        obj=sensor_model)
            logging.info('preprocessor object and model saved')
            model_trainer_artifacts=ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.model_trained_object_file_path,
                test_metrics_artifact=classification_test_metrics,
                train_metrics_artifact=classification_train_metrics
            )
            return model_trainer_artifacts
        except Exception as e:
            raise MLException(e,sys)
        
        

        

    

