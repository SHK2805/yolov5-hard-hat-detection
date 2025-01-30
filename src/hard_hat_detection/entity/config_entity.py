from dataclasses import dataclass
from pathlib import Path


@dataclass
class DataIngestionConfig:
    # these are the inputs to the data ingestion pipeline
    data_root_dir: Path
    roboflow_api_key_file: Path
    roboflow_workspace: str
    roboflow_project: str
    roboflow_version: str
    roboflow_export_format: str
    roboflow_api_key: str

@dataclass
class DataValidationConfig:
    # these are the inputs to the data validation pipeline
    data_root_dir: Path
    data_dir: Path
    STATUS_FILE: str
    # folders
    TRAIN_DIR: str
    VAL_DIR: str
    TEST_DIR: str
    IMG_DIR: str
    LABEL_DIR: str
    LABELS_FILE_EXT: str
    # files
    DATA_FILE: str

@dataclass
class DataTransformationConfig:
    # paths
    data_root_dir: Path
    # inputs
    data_dir: Path
    # outputs
    # folders
    TRAIN_DIR: str
    VAL_DIR: str
    TEST_DIR: str
    IMG_DIR: str
    LABEL_DIR: str
    IMG_FILE_EXT: str
    LABELS_FILE_EXT: str

@dataclass
class ModelTrainerConfig:
    # paths
    data_root_dir: str
    # inputs
    data_dir: str
    input_yaml_path: str
    # outputs
    output_yaml_path: str
    # folders
    TRAIN_DIR: str
    VAL_DIR: str
    TEST_DIR: str
    model_root_path: str
    used_model_name: str
    weight_name: str
    no_epochs: int
    batch_size: int

@dataclass
class ModelEvaluationConfig:
    # these are the inputs to the model evaluation pipeline
    data_root_dir: str
    data_dir: str
    input_yaml_path: str
    weights_path: str
    model_root_path: str
    used_model_name: str
    batch_size: int