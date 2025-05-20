import os
import sys
from Heart_Disease_Prediction.entity.config_entity import DataValidationConfig
from Heart_Disease_Prediction.exception.exception import HeartDiasesException
from Heart_Disease_Prediction.logging.logging import logging
from Heart_Disease_Prediction.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
import pandas as pd
from scipy.stats import ks_2samp
from Heart_Disease_Prediction.constant.training_pipeline import SCHEMA_FILE_PATH
from Heart_Disease_Prediction.utils.main_utils.utils import read_yaml_file,write_yaml_file
class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise HeartDiasesException(e,sys)
        
    def read_data(self,file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise HeartDiasesException(e,sys)
        
    def validated_number_of_cols(self,dataframe):
        try:
           
            number_of_cols=len(dataframe)
            if number_of_cols==len(SCHEMA_FILE_PATH):
                return True
            else:
                return False
        except Exception as e:
            raise HeartDiasesException(e,sys)
        
    def drift_report(self,base_df,current_df,threshold=0.5):
        try:
            status=True
            report={

            }
            for col in base_df.columns:
                d1=base_df[col]
                d2=current_df[col]
                is_same_dist=ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False

                report.update({col:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
                
                drift_report_file_path=self.data_validation_config.data_validation_report_dir
                os.makedirs(os.path.dirname(drift_report_file_path),exist_ok=True)
                write_yaml_file(drift_report_file_path,content=report)
        except Exception as e:
            raise HeartDiasesException(e,sys)
        


    def inititae_data_validation(self):
        try:
            train_data=self.data_ingestion_artifact.train_file_name
            test_data=self.data_ingestion_artifact.test_file_name

            # read the data from function
            train_df=self.read_data(train_data)
            test_df=self.read_data(test_data)

            logging.info(f"check the avalidation cols")
            status=self.validated_number_of_cols(train_df)
            if not status:
                logging.info(f"train data has not all cols {train_df.shape}")
            
            status=self.validated_number_of_cols(test_df)
            if not status:
                logging.info(f"test data has not all cols:{test_df.shape}")


            logging.info("call the drift report dir")
            status=self.drift_report(train_df,test_df)

            os.makedirs(os.path.dirname(self.data_validation_config.data_validation_valid_train_file),exist_ok=True)
            logging.info("pass the train and test data into valid file path")
            train_df.to_csv(self.data_validation_config.data_validation_valid_train_file)
            test_df.to_csv(self.data_validation_config.data_validation_valid_test_file)

            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                data_validation_train_file=self.data_validation_config.data_validation_valid_train_file,
                data_validation_test_file=self.data_validation_config.data_validation_valid_test_file,
                data_validation_report_drift_file=self.data_validation_config.data_validation_report_dir,
                data_validation_invalid_train_file=None,
                data_validation_invalid_test_file=None

            )

            return data_validation_artifact
        except Exception as e:
            raise HeartDiasesException(e,sys)
        








