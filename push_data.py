import os
import sys
import pandas as pd
import pymongo
from dotenv import load_dotenv

# Uncomment these if you have your own custom exception and logging modules
from Heart_Disease_Prediction.exception.exception import HeartDiasesException
from Heart_Disease_Prediction.logging.logging import logging

load_dotenv()  # load environment variables from .env

MONGO_DB_URL = os.getenv('MONGO_DB_URL')

# # Simple logging substitute if you don't have custom logger
# def log_info(msg):
#     print("[INFO]", msg)

class HeartDataExtract:
    def __init__(self):
        try:
            # No init needed currently
            pass
        except Exception as e:
            # raise HeartDiasesException(e, sys)
            print("Error in __init__:", e)
            raise

    def csv_to_json(self, dataframe_path):
        try:
            logging.info(f"Reading CSV file: {dataframe_path}")
            df = pd.read_csv(dataframe_path)
            logging.info(f"CSV file read successfully with shape: {df.shape}")

            # Drop _id column if exists (to avoid MongoDB conflict)
            if "_id" in df.columns:
                df.drop(columns="_id", inplace=True)
                logging.info("Dropped '_id' column from dataframe")

            df.reset_index(drop=True, inplace=True)

            # Convert dataframe to list of dicts for MongoDB insertion
            records = df.to_dict(orient='records')
            return records
        except Exception as e:
            # raise HeartDiasesException(e, sys)
            print("Error in csv_to_json:", e)
            raise

    def insert_data_into_mongodb(self, records, database, collection):
        try:
            if not MONGO_DB_URL:
                raise Exception("MONGO_DB_URL environment variable is not set or empty")

            logging.info(f"Connecting to MongoDB...")
            mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            # Test connection
            mongo_client.admin.command('ping')
            logging.info("MongoDB connected successfully!")

            db = mongo_client[database]
            coll = db[collection]

            result = coll.insert_many(records)
            logging.info(f"Inserted {len(result.inserted_ids)} records into MongoDB collection '{collection}'")

            return len(result.inserted_ids)
        except Exception as e:
            # raise HeartDiasesException(e, sys)
            print("Error in insert_data_into_mongodb:", e)
            raise


if __name__ == "__main__":
    try:
        file_path = r"D:\RESUME ML PROJECTS\Heart Disease Prediction\Heart_Data\heart.csv"
        database_name = "sharmi"
        collection_name = "Heart_Data"

        heart_data_extract = HeartDataExtract()
        records = heart_data_extract.csv_to_json(file_path)

        number_of_records = heart_data_extract.insert_data_into_mongodb(records, database_name, collection_name)

        print(f"Total records inserted: {number_of_records}")

    except Exception as e:
        
        raise HeartDiasesException(e,sys)
