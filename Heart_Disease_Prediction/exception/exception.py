import os
import sys
from Heart_Disease_Prediction.logging.logging import logging


logging.info("create the own exception classs")

logging.info("it contains two params like error message and error deatils {filename and fileno}")


class HeartDiasesException(Exception):
    def __init__(self,error_message,error_detail:sys):

        self.error_message=error_message
        _,_,exc_tb=error_detail.exc_info()

        self.lineno=exc_tb.tb_lineno
        self.file_name=exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        self.file_name, self.lineno, str(self.error_message))

        
if __name__=="__main__":
    try:
        a=1/0
    except Exception as e:
      raise HeartDiasesException(e,sys)