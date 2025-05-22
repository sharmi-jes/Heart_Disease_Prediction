import os
import sys
from Heart_Disease_Prediction.exception.exception import HeartDiasesException
from Heart_Disease_Prediction.logging.logging import logging

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:

          self.preprocessor=preprocessor
          self.model=model

        except Exception as e:
           raise HeartDiasesException(e,sys)
        
    def predict(self,x):
       try:
           x_preprocessor=self.preprocessor.transform(x)
           y_hat=self.model.predict(x_preprocessor)
           return y_hat
       except Exception as e:
          raise HeartDiasesException(e,sys)