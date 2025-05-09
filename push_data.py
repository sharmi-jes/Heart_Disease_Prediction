import os
import sys
import pandas as pd
import json
import numpy as np
from Heart_Disease_Prediction.exception.exception import HeartDiasesException
from Heart_Disease_Prediction.logging.logging import logging
import pymongo

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv('MONGO_DB_URL')


logging.info("create the heart data extract class")
class HeartDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise HeartDiasesException(e,sys)

    logging.info("create the function which performe like tpo convert csv to json format data")    
    def csv_to_json(self,dataframe):
        try:
            df=pd.read_csv(dataframe)
            if "_id" in df.columns:
                df=df.drop(columns="_id",inplace=True)
            df.reset_index(inplace=True)
            logging.info("transpose the data and convert in into json format {records}")

            records=list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise HeartDiasesException(e,sys)
    logging.info("pass the data into mongodb")    
    def insert_data_into_mongodb(self,records,database,collection):
        try:
            self.records=records
            self.collection=collection
            self.database=database
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)

             # Test the connection
            self.mongo_client.admin.command('ping')  # Pings the MongoDB server to check if it's up
            logging.info("MongoDB connected successfully!")

            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]

            self.collection.insert_many(self.records)
            return len(self.records)
        
        except Exception as e:
            raise HeartDiasesException(e,sys)
        
if __name__=="__main__":
    try:
        file_path="D:\RESUME ML PROJECTS\Heart Disease Prediction\Heart_Data\heart.csv"
        database_name="sharmianyum"
        collection_name="Heart_Data"
        heart_data_extract=HeartDataExtract()
        records=heart_data_extract.csv_to_json(file_path)
        number_of_records=heart_data_extract.insert_data_into_mongodb(records,database_name,collection_name)
        print(number_of_records)
    except Exception as e:
        raise HeartDiasesException(e,sys)



