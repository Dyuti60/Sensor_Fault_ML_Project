import pymongo
from dotenv import load_dotenv
from SensorFaultPrediction.constant.databases import DATABASE_NAME
from SensorFaultPrediction.constant.env_variables import MONGO_URL_KEY
import certifi
import os
load_dotenv()
ca = certifi.where()

'''
Install pymongo and certifi in order to securely connect with mongo client
Define Class MongoDBClient and initialize 

set mongo_db_url and cerftifi.where()
if url is having localhost then tlsCAFile is not required else it is required

mongo_db_url needs to be passed on pymongo.MongoClient

initialise client, database
'''

class MongoDBClient:
    client = None
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:

            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGO_URL_KEY)
                print(mongo_db_url)
                if "localhost" in mongo_db_url:
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url) 
                else:
                    MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise e


