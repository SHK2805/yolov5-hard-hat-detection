import sys
from pathlib import Path

from src.hard_hat_detection.components.data_transformation import DataTransformation
from src.hard_hat_detection.config.configuration import ConfigurationManager
from src.hard_hat_detection.exception.exception import CustomException
from src.hard_hat_detection.logger.logger_config import logger
from src.hard_hat_detection.utils.common import check_file_exists

STAGE_NAME: str = "Data Transformation Pipeline"
class DataTransformationTrainingPipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__
        self.stage_name = STAGE_NAME

    def data_transformation(self):
        tag: str = f"{self.class_name}::data_transformation::"
        try:
            # check the 'artifacts/data_validation/status.txt' file to see if the data validation pipeline was successful
            logger.info(f"{tag}::Checking if the data validation pipeline was successful")
            data_validation_config = ConfigurationManager().get_data_validation_config()

            # check if the status file exists and read the file
            if not check_file_exists(Path(data_validation_config.STATUS_FILE)):
                message: str = f"Data validation status file {data_validation_config.STATUS_FILE} not found"
                logger.error(f"{tag}::{message}")
                raise Exception(f"{message}")

            with open(Path(data_validation_config.STATUS_FILE), "r") as file:
                # The current format of the status file is just the text True or False but this can tbe updated to
                # New Format as below and this code supports that
                # Validation Status: True
                # the [-1] will give the last element of the list which is the status
                data_validation_status = file.read().split(" ")[-1]
                if data_validation_status != "True":
                    message: str = f"Data validation pipeline was not successful. Status: {data_validation_status}"
                    logger.error(f"{tag}::{message}")
                    raise Exception(f"{message}")

            logger.info(f"{tag}::Data validation pipeline was successful")
            config = ConfigurationManager()
            logger.info(f"{tag}::Configuration Manager object created")

            data_transformation_config = config.get_data_transformation_config()
            logger.info(f"{tag}::Data transformation configuration obtained")

            data_transformation = DataTransformation(config=data_transformation_config)
            logger.info(f"{tag}::Data transformation object created")

            logger.info(f"{tag}::Running the data transformation pipeline")
            data_transformation.transform()
            logger.info(f"{tag}::Data transformation pipeline completed")
        except Exception as e:
            logger.error(f"{tag}::Error running the data transformation pipeline: {e}")
            raise CustomException(e, sys)