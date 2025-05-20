from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    train_file_name:str
    test_file_name:str