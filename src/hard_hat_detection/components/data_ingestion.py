import os

from src.hard_hat_detection.entity.config_entity import DataIngestionConfig
from src.hard_hat_detection.logger.logger_config import logger
from roboflow import Roboflow

from src.hard_hat_detection.utils.common import get_env_var


class DataIngestion:
    def __init__(self,config: DataIngestionConfig):
        self.class_name = self.__class__.__name__
        self.config: DataIngestionConfig = config

    # There is a limit to the number of times you can download data from Roboflow.
    # If you have already downloaded the data, you can skip this step.
    def download_data(self):
        tag: str = f"{self.class_name}::download_data::"
        logger.info(f"{tag}Downloading data from Roboflow")
        download_data = False
        if download_data:
            rf = Roboflow(api_key=self.config.roboflow_api_key)
            project = rf.workspace(self.config.roboflow_workspace).project(self.config.roboflow_project)
            version = project.version(self.config.roboflow_version)
            dataset = version.download(model_format=str(self.config.roboflow_export_format),
                                       location=str(self.config.data_root_dir),
                                       overwrite=True)
            logger.info(f"{tag}Data downloaded into the directory: {self.config.data_root_dir} "
                        f"in the format: {self.config.roboflow_export_format} with overwrite: {True}")

            return dataset
        else:
            logger.warning(f"{tag}Data already downloaded. Skipping the download step")
            return None



