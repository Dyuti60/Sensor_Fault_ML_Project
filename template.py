import os
from pathlib import Path

import logging
logging.basicConfig(level=logging.INFO)

project_name='SensorFaultPrediction'

list_of_files=[
    f'{project_name}/__init__.py',
    f'{project_name}/exception.py',
    f'{project_name}/logger.py',
    f'{project_name}/entity/__init__.py',
    f'{project_name}/entity/artifact_entity.py',
    f'{project_name}/entity/config_entity.py',
    f'{project_name}/ml/__init__.py',
    f'{project_name}/ml/metric/__init__.py',
    f'{project_name}/ml/metric/classification_metrics.py',
    f'{project_name}/ml/model/__init__.py',
    f'{project_name}/ml/model/estimator.py',
    f'{project_name}/pipeline/__init__.py',
    f'{project_name}/pipeline/training_pipeline.py',
    f'{project_name}/pipeline/prediction_pipeline.py',
    f'{project_name}/components/__init__.py',
    f'{project_name}/components/data_ingestion.py',
    f'{project_name}/components/data_transformation.py',
    f'{project_name}/components/data_validation.py',
    f'{project_name}/components/model_evaluation.py',
    f'{project_name}/components/model_pusher.py',
    f'{project_name}/components/model_trainer.py',
    f'{project_name}/components/model_monitoring.py',
    f'{project_name}/constant/__init__.py',
    f'{project_name}/constant/applications.py',
    f'{project_name}/constant/databases.py',
    f'{project_name}/constant/env_variables.py',
    f'{project_name}/constant/s3_bucket.py',
    f'{project_name}/data_access/__init__.py',
    f'{project_name}/data_access/sensor_data.py',
    f'{project_name}/cloud_storage/__init__.py',
    f'{project_name}/cloud_storage/s3_syncer.py',
    f'{project_name}/utils/__init__.py',
    f'{project_name}/utils/mail_utils.py',
    f'{project_name}/configuration/__init__.py',
    f'{project_name}/configuration/mongodb_connector.py',
    'Dockerfile',
    '.dockerfile',
    'docker-compose.yml',
    'README.md',
    '.gitignore',
    '.dockerignore',
    '.env',
    'requirements.txt',
    'setup.py'
]

for filepath in list_of_files:
    filepath=Path(filepath)
    filedir,filename=os.path.split(filepath)


    #creates directory only if not exists or doesnot creates
    if filedir !='':
        os.makedirs(filedir,exist_ok=True)
        logging.info(f'Directory {filedir} for file - {filename} created')


    #checks if filepath doesn't exists or if filepath size is zero then, create empty file else does nothing
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,'w') as file_obj:
            pass
            logging.info(f'creating empty file :{filepath}')
    else:
        logging.info(f'File {filename} already exists')