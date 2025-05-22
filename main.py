import os
import sys
from Heart_Disease_Prediction.exception.exception import HeartDiasesException
from Heart_Disease_Prediction.logging.logging import logging
from Heart_Disease_Prediction.components.data_ingestion import DataIngestion
from Heart_Disease_Prediction.components.data_validation import DataValidation
from Heart_Disease_Prediction.components.data_transformation import DataTransformation
from Heart_Disease_Prediction.components.model_trainer import ModelTrainer
from Heart_Disease_Prediction.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig,DataValidationConfig,DataTransformationconfig,ModelTrainerConfig
from Heart_Disease_Prediction.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact


if __name__=="__main__":
    try:
        logging.info("start the data ingetion process")
        training_pipeline=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline)
        data_ingestion=DataIngestion(data_ingestion_config)
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info(f"completed the data ingestion processs {data_ingestion_artifact}")


        logging.info("Starting the data validation process")
        data_validation_config=DataValidationConfig(training_pipeline)
        data_validation=DataValidation(data_ingestion_artifact,data_validation_config)
        data_validation_artifact=data_validation.inititae_data_validation()
        print(data_validation_artifact)
        logging.info("compledte the process of data validation")


        logging.info("starting the process of data transformation")
        data_transformation_config=DataTransformationconfig(training_pipeline)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
        logging.info(f"complete the process of data transformation artifact {data_transformation_artifact}")


        logging.info("starting the process of model trainer")
        model_trainer_config=ModelTrainerConfig(training_pipeline)
        model_trainer=ModelTrainer(data_transformation_artifact,model_trainer_config)
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        print(model_trainer_artifact)
        logging.info(f"completed the process of model trainer:{model_trainer_artifact}")
    except Exception as e:
        raise HeartDiasesException(e,sys)
    