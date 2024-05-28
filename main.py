from SensorFaultPrediction.pipeline.training_pipeline import TrainingPipeline
from SensorFaultPrediction.exception import MLException
from SensorFaultPrediction.logger import logging
import os, sys
from fastapi import FastAPI, File, UploadFile
from SensorFaultPrediction.constant.applications import APP_HOST,APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from SensorFaultPrediction.ml.model.estimator import ModelResolver,TargetValueMapping
from SensorFaultPrediction.utils.mail_utils import load_object
from fastapi.middleware.cors import CORSMiddleware

app=FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/',tags=['authentication'])
async def index():
    return RedirectResponse(url='/docs')

@app.get("/train")
async def train_route():
    try:

        train_pipeline = TrainingPipeline()
        if train_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        train_pipeline.run_train_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

def main():
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.run_train_pipeline()
    except Exception as e:
        raise MLException(e,sys)
    
if __name__ == '__main__':
    main()
    app_run(app,host=APP_HOST, port=APP_PORT)

#pendulum
#apache-airflow