import os
from SensorFaultPrediction.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_TRAINER_TRAINED_MODEL_NAME
class TargetValueMapping:
    def __init__(self):
        self.neg:int=0
        self.pos:int=1

    def to_dict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        mapping=self.to_dict()
        return dict(zip(mapping.values(),mapping.keys()))

class SensorModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise e
    def predict(self,X):
        try:
            x_transform=self.preprocessor.transform(X)
            y_pred=self.model.predict(x_transform)
            return y_pred
        except Exception as e:
            raise e
        

class ModelResolver:

    def __init__(self,model_dir=SAVED_MODEL_DIR):
        try:
            self.model_dir = model_dir

        except Exception as e:
            raise e

    def get_best_model_path(self)->str:
        try:
            timestamps = list(map(int,os.listdir(self.model_dir)))
            latest_timestamp = max(timestamps)
            latest_model_path= os.path.join(self.model_dir,f"{latest_timestamp}",MODEL_TRAINER_TRAINED_MODEL_NAME)
            return latest_model_path
        except Exception as e:
            raise e

    def is_model_exists(self)->bool:
        try:
            if not os.path.exists(self.model_dir):
                return False

            timestamps = os.listdir(self.model_dir)
            if len(timestamps)==0:
                return False
            
            latest_model_path = self.get_best_model_path()

            if not os.path.exists(latest_model_path):
                return False

            return True
        except Exception as e:
            raise e

