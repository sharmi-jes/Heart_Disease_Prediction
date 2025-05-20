import os
import sys
from Heart_Disease_Prediction.exception.exception import HeartDiasesException
from Heart_Disease_Prediction.logging.logging import logging
from Heart_Disease_Prediction.constant import training_pipeline
from datetime import datetime

logging.info("create the trainig pipeline config class")
class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=timestamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name=training_pipeline.PIPELINE_NAME
        self.artifact_name=training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact_name,timestamp)
        # self.model_dir=os.path.join("final_model")
        self.timestamp: str=timestamp

logging.info("create the data ingestion config class for data ingestion")
class DataIngestionConfig:
    def __init__(self,training_pipelineconfig:TrainingPipelineConfig):
        self.data_ingestion_dir:str=os.path.join(training_pipelineconfig.artifact_dir,training_pipeline.DATA_INGESTION_DIR)
        self.data_ingestion_ingested_dir:str=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_INGESTED_DIR)
        self.feature_store_path:str=os.path.join(self.data_ingestion_dir,training_pipeline.DATA_INGESTION_FEATURE_STORE_PATH)
        self.data_ingestion_split_ration_data=training_pipeline.DATA_INGESTION_SPLIT_RATIO
        self.data_ingestion_database_name=training_pipeline.DATA_INGESTION_DATABASE_NAME
        self.data_ingestion_collection_name=training_pipeline.DATA_INGESTION_COLLECTION_NAME

        self.train_file=training_pipeline.TRAIN_FILE_NAME
        self.test_file=training_pipeline.TEST_FILE_NAME