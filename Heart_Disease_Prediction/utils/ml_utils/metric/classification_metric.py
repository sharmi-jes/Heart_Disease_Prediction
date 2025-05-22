import os
import sys
from Heart_Disease_Prediction.entity.artifact_entity import ClassificationMetric
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score
from Heart_Disease_Prediction.exception.exception import HeartDiasesException

#  f1_score:float
    # accuracy_score:float
    # precision:float
    # recall:float
def get_classification_score(y_true,y_pred):
    try:
     f1score=f1_score(y_true,y_pred)
     accuracy=accuracy_score(y_true,y_pred)
     precision=precision_score(y_true,y_pred)
     recall=recall_score(y_true,y_pred)

     classification_metric=ClassificationMetric(f1_score=f1score,accuracy_score=accuracy,precision=precision,recall=recall)
     return classification_metric
    except Exception as e:
       raise HeartDiasesException(e,sys)
