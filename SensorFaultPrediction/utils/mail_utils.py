import numpy as np
import yaml
import dill
import os, sys
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging

# for yaml file, to read yaml.safe_load(file); to write yaml file yaml.dump(file); read_yaml_file returns dict
# for numpy array, to save np.save(file, array); to load numpy array np.load(file); load_numpy_array returns np.array
# for saving object - dill.dump(obj,file); for loading objects - dill.load(obj,file); load_object returns object
def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise MLException(e,sys)

def write_yaml_file(file_path:str, content:object,replace:bool=False)-> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as yaml_file:
            yaml.dump(content,yaml_file)
    except Exception as e:
        raise MLException(e,sys)

def save_numpy_array_data(file_path:str,array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise MLException(e,sys)

def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise MLException(e,sys)

def save_object(file_path:str,obj:object)->None:
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            dill.dump(obj,file_obj)
    except Exception as e:
        raise MLException(e,sys)

def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception("File path : {} doest not exist".format(file_path))
        with open(file_path, 'rb') as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise MLException(e,sys)
    
    