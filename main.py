import os
import sys
from Heart_Disease_Prediction.exception.exception import HeartDiasesException
from Heart_Disease_Prediction.logging.logging import logging
from Heart_Disease_Prediction.components.data_ingestion import DataIngestion
from Heart_Disease_Prediction.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig
from Heart_Disease_Prediction.entity.artifact_entity import DataIngestionArtifact


if __name__=="__main__":
    try:
        logging.info("start the data ingetion process")
        training_pipeline=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline)
        data_ingestion=DataIngestion(data_ingestion_config)
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info(f"completed the data ingestion processs {data_ingestion_artifact}")
    except Exception as e:
        raise HeartDiasesException(e,sys)
    