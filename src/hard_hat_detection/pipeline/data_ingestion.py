import sys

from src.hard_hat_detection.components.data_ingestion import DataIngestion
from src.hard_hat_detection.config.configuration import ConfigurationManager
from src.hard_hat_detection.exception.exception import CustomException
from src.hard_hat_detection.logger.logger_config import logger

STAGE_NAME: str = "Data Ingestion Pipeline"
class DataIngestionTrainingPipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__
        self.stage_name = STAGE_NAME

    def data_ingestion(self) -> None:
        tag: str = f"{self.class_name}::data_ingestion::"
        try:
            config = ConfigurationManager()
            logger.info(f"{tag}::Configuration Manager object created")

            data_ingestion_config = config.get_data_ingestion_config()
            logger.info(f"{tag}::Data ingestion configuration obtained")

            data_ingestion = DataIngestion(config=data_ingestion_config)
            logger.info(f"{tag}::Data ingestion object created")

            logger.info(f"{tag}::Running the data ingestion pipeline")

            data_ingestion.download_data()
            logger.info(f"{tag}::Data downloaded successfully")
        except Exception as e:
            logger.error(f"{tag}::Error running the data ingestion pipeline: {e}")
            raise CustomException(e, sys)
