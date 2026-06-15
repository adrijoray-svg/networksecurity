import os
import sys
import json
from dotenv import load_dotenv
load_dotenv()

mongo_db_url = os.getenv("MONGO_DB_URL")
print(mongo_db_url)

import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
    def csv_to_json_converter(self,file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise CustomException(e,sys)
    def insert_data_mongodb(self,records,database,collections):
        try:
            self.database = database
            self.records = records
            self.collection = collections

            self.mongoclient = pymongo.MongoClient(mongo_db_url)
            self.database = self.mongoclient[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise CustomException(e,sys)
    
if __name__ == '__main__':
    file_path = "network_data\phisingData.csv"
    database = "AdrijoProject"
    collections = "NetworkData"
    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json_converter(file_path)
    no_of_records = network_obj.insert_data_mongodb(records,database,collections)
    print(no_of_records)
