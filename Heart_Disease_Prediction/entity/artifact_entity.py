from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    train_file_name:str
    test_file_name:str

@dataclass
class DataValidationArtifact:
    validation_status:bool
    data_validation_train_file:str
    data_validation_test_file:str
    data_validation_invalid_train_file:str
    data_validation_invalid_test_file:str
    data_validation_report_drift_file:str
    