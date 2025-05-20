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

load_dotenv()

MONGO_DB_URL = os.getenv('MONGO_DB_URL')
print(MONGO_DB_URL)





class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise HeartDiasesException(e, sys)

    def get_data_from_mongodb(self):
        logging.info("Getting data from MongoDB")
        try:
            database_name = self.data_ingestion_config.data_ingestion_database_name
            collection_name = self.data_ingestion_config.data_ingestion_collection_name
            self.pymongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.pymongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))

            if "_id" in df.columns:
                df = df.drop(columns="_id", axis=1)

            df.reset_index(drop=True, inplace=True)
            return df
        except Exception as e:
            raise HeartDiasesException(e, sys)

    def feature_store_path(self, dataframe):
        logging.info("Storing the data in the feature store path")
        try:
            feature_store_path = self.data_ingestion_config.feature_store_path
            dirname = os.path.dirname(feature_store_path)
            os.makedirs(dirname, exist_ok=True)
            dataframe.to_csv(feature_store_path, index=False)
        except Exception as e:
            raise HeartDiasesException(e, sys)

    def feature_split_data(self, dataframe):
        logging.info("Splitting the data into train and test")
        try:
            train_data, test_data = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.data_ingestion_split_ration_data
            )

            dir_path = os.path.dirname(self.data_ingestion_config.train_file)
            os.makedirs(dir_path, exist_ok=True)

            train_data.to_csv(self.data_ingestion_config.train_file, index=False)
            test_data.to_csv(self.data_ingestion_config.test_file, index=False)
        except Exception as e:
            raise HeartDiasesException(e, sys)

    def initiate_data_ingestion(self):
        logging.info("Initiating data ingestion process")
        try:
            dataframe = self.get_data_from_mongodb()
            self.feature_store_path(dataframe)
            self.feature_split_data(dataframe)
            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.train_file,
                test_file_path=self.data_ingestion_config.test_file
            )
            return data_ingestion_artifact
        except Exception as e:
            raise HeartDiasesException(e, sys)
