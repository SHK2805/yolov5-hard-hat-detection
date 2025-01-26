from src.hard_hat_detection.components.data_validation import DataValidation
from src.hard_hat_detection.config.configuration import ConfigurationManager
from src.hard_hat_detection.logger.logger_config import logger

STAGE_NAME: str = "Data Validation Pipeline"
class DataValidationTrainingPipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__
        self.stage_name = STAGE_NAME

    def data_validation(self) -> None:
        tag: str = f"{self.class_name}::data_validation::"
        try:
            config = ConfigurationManager()
            logger.info(f"{tag}::Configuration Manager object created")

            data_validation_config = config.get_data_validation_config()
            logger.info(f"{tag}::Data validation configuration obtained")

            data_validation = DataValidation(config=data_validation_config)
            logger.info(f"{tag}::Data validation object created")

            logger.info(f"{tag}::Running the data validation pipeline")

            if not data_validation.validate():
                message: str = f"Data validation failed"
                logger.error(f"{tag}::{message}")
                raise Exception(f"{message}")

            logger.info(f"{tag}::All files validated successfully")
        except Exception as e:
            logger.error(f"{tag}::Error running the data validation pipeline: {e}")
            raise e