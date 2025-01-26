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