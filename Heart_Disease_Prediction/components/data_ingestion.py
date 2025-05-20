import os
import sys
from Heart_Disease_Prediction.exception.exception import HeartDiasesException
from Heart_Disease_Prediction.logging.logging import logging
from Heart_Disease_Prediction.entity.config_entity import DataIngestionConfig
import pymongo
from sklearn.model_selection import train_test_split
import pandas as pd
from Heart_Disease_Prediction.entity.artifact_entity import DataIngestionArtifact
from dotenv import load_dotenv
import numpy as np
load_dotenv()

MONGO_DB_URL = os.getenv('MONGO_DB_URL')
print(MONGO_DB_URL)


logging.info("create the data ingestion class")
class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise HeartDiasesException(e,sys)

    logging.info("read the data from mongodb")    
    def read_data_from_mongodb(self):
        try:
            database=self.data_ingestion_config.data_ingestion_database_name
            collection=self.data_ingestion_config.data_ingestion_collection_name
            self.mongoclient=pymongo.MongoClient(MONGO_DB_URL)

            collection=self.mongoclient[database][collection]

            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns:
                df=df.drop(columns="_id")
            df.replace({"na":np.nan},inplace=True)
            logging.info(f"shape of data is {df.shape}")
            return df
        
        except Exception as e:
            raise HeartDiasesException(e,sys)
        

    def feature_store_path(self,dataframe):
        try:
            feature_store_path=self.data_ingestion_config.feature_store_path

            os.makedirs(os.path.dirname(feature_store_path),exist_ok=True)

            dataframe.to_csv(feature_store_path,index=False,header=True)

            return dataframe

        except Exception as e:
            raise HeartDiasesException(e,sys)
    logging.info("split the data as train and test")    
    def split_data_as_train_test(self,dataframe):
        try:
            train_data,test_data=train_test_split(dataframe,test_size=self.data_ingestion_config.data_ingestion_split_ration_data)
            

            logging.info("create a directory for triain and test data")
            dir_path = os.path.dirname(self.data_ingestion_config.data_ingestion_train_file)
            
            os.makedirs(dir_path, exist_ok=True)
            


            logging.info("pass the data into train and test")

            train_data.to_csv(self.data_ingestion_config.data_ingestion_train_file,index=False, header=True)
            test_data.to_csv(self.data_ingestion_config.data_ingestion_test_file,index=False, header=True)

            # return train_data,test_data


            
        except Exception as e:
            raise HeartDiasesException(e,sys)
        

    def initiate_data_ingestion(self):
        dataframe=self.read_data_from_mongodb()
        dataframe=self.feature_store_path(dataframe)
        dataframe=self.split_data_as_train_test(dataframe)
        data_ingestion_artifact=DataIngestionArtifact(
                train_file_name=self.data_ingestion_config.data_ingestion_train_file,
                test_file_name=self.data_ingestion_config.data_ingestion_test_file
            )
        return data_ingestion_artifact