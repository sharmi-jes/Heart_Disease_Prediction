import os
import sys
from datetime import datetime
import logging


# create the logs timeline 
LOG_FILE_PATH=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


# create a directory folder logs
log_path=os.path.join(os.getcwd(),"logs")
os.makedirs(log_path,exist_ok=True)

# join the log path and log file path
log_file_path=os.path.join(log_path,LOG_FILE_PATH)


# logging the info
logging.basicConfig(
    filename=log_file_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)