import os
import sys
import numpy as np
import pandas as pd
from Heart_Disease_Prediction.exception.exception import HeartDiasesException
from Heart_Disease_Prediction.logging.logging import logging
from Heart_Disease_Prediction.entity.config_entity import DataTransformationconfig
from Heart_Disease_Prediction.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from Heart_Disease_Prediction.constant.training_pipeline import TARGET_VARIABLE
from sklearn.preprocessing import StandardScaler
from Heart_Disease_Prediction.utils.main_utils.utils import save_object,save_numpy_array_data


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationconfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_confog=data_transformation_config
        except Exception as e:
            raise HeartDiasesException(e,sys)
        
    def read_data(self,filepath):
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise HeartDiasesException(e,sys)
        
    def scaled_data(self):
        try:
            return StandardScaler()
        except Exception as e:
            raise HeartDiasesException(e,sys)
        
        

    def initiate_data_transformation(self):
        try:
            train_data=self.data_validation_artifact.data_validation_train_file
            test_data=self.data_validation_artifact.data_validation_test_file

            logging.info(f"read the data from the function")
            train_df=self.read_data(train_data)
            test_df=self.read_data(test_data)

            logging.info(f"The shape of train data is:{train_df.shape} and test data is:{test_df.shape}")
            logging.info(f"the train data cols is:{train_df.columns}")

            logging.info("remove the target from both train and test data")
            input_feature_train_df=train_df.drop(columns=[TARGET_VARIABLE,'Unnamed: 0'])
            input_feature_train_target_df=train_df[TARGET_VARIABLE]

            input_feature_test_df=test_df.drop(columns=[TARGET_VARIABLE,'Unnamed: 0'])
            input_feature_test_target_df=test_df[TARGET_VARIABLE]


            logging.info("scaled data for train and test")

            preprocesssing=self.scaled_data()
            input_feature_train_sacled_df=preprocesssing.fit_transform(input_feature_train_df)
            input_feature_test_scaled_df=preprocesssing.transform(input_feature_test_df)

            save_object(self.data_transformation_confog.data_transformation_object_dir,preprocesssing)
            save_object("final_model/preprocessing.pkl",preprocesssing)

            logging.info("combine the i/p and o/p data")
            train_array=np.c_[input_feature_train_sacled_df,np.array(input_feature_train_target_df)]
            test_array=np.c_[input_feature_test_scaled_df,np.array(input_feature_test_target_df)]

            logging.info(f"shape of after combining data is {train_array.shape} and {test_array.shape}")


            logging.info("save data in the form of numpy array")
            save_numpy_array_data(self.data_transformation_confog.data_transformation_train_file,train_array)
            save_numpy_array_data(self.data_transformation_confog.data_transformation_test_file,test_array)

            logging.info("save the data transformation artifact")
            data_transformation_artifact=DataTransformationArtifact(
                data_transformation_train_file=self.data_transformation_confog.data_transformation_train_file,
                data_transformation_test_file=self.data_transformation_confog.data_transformation_test_file,
                data_transformation_object_dir=self.data_transformation_confog.data_transformation_object_dir

            )

            return data_transformation_artifact
        except Exception as e:
            raise HeartDiasesException(e,sys)
        









