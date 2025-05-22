import os
import sys
from Heart_Disease_Prediction.exception.exception import HeartDiasesException
from Heart_Disease_Prediction.logging.logging import logging
from Heart_Disease_Prediction.utils.main_utils.utils import load_object
import pandas as pd

class PredictPipeline:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise HeartDiasesException(e,sys)
        
    def predict(self,features):
        try:
            model_path='final_model/model.pkl'
            preprocessor_path="final_model/preprocessing.pkl"
            model=load_object(model_path)
            preprocessor=load_object(preprocessor_path)
            # if "- Unnamed: 0" in features.columns:
            #     features.drop(columns="- Unnamed: 0",axis=1)
            transform_features=preprocessor.transform(features)
            y_pred=model.predict(transform_features)
            return y_pred
        except Exception as e:
            raise HeartDiasesException(e,sys)
        
# age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal,target
# 43,1,0,115,303,0,1,181,0,1.2,1,0,2,1
# 35,0,0,138,183,0,1,182,0,1.4,2,0,2,1

class CustomData:
    def __init__(self,age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal):
        self.age=age
        self.sex=sex
        self.cp=cp
        self.trestbps=trestbps
        self.chol=chol
        self.fbs=fbs
        self.restecg=restecg
        self.thalach=thalach
        self.exang=exang
        self.oldpeak=oldpeak
        self.slope=slope
        self.ca=ca
        self.thal=thal

    def get_data_as_dataframe(self):
        try:
         input_data = {
            "age": [self.age],
            "sex": [self.sex],
            "cp": [self.cp],
            "trestbps": [self.trestbps],
            "chol": [self.chol],
            "fbs": [self.fbs],
            "restecg": [self.restecg],
            "thalach": [self.thalach],
            "exang": [self.exang],
            "oldpeak": [self.oldpeak],
            "slope": [self.slope],
            "ca": [self.ca],
            "thal": [self.thal]
         }

         df = pd.DataFrame(input_data)

        #  if "Unnamed: 0" in df.columns:
        #     df.drop("Unnamed: 0", axis=1, inplace=True)

         return df
        except Exception as e:
          raise HeartDiasesException(e, sys)

      


