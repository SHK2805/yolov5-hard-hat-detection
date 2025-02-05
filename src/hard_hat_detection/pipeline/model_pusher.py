import sys

from src.hard_hat_detection.components.model_pusher import ModelPusher
from src.hard_hat_detection.config.configuration import ConfigurationManager
from src.hard_hat_detection.exception.exception import CustomException
from src.hard_hat_detection.logger.logger_config import logger

STAGE_NAME: str = "Model Pusher Pipeline"
class ModelPusherTrainingPipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__
        self.stage_name = STAGE_NAME

    def model_pusher(self) -> None:
        tag: str = f"{self.class_name}::model_pusher::"
        try:
            config = ConfigurationManager()
            logger.info(f"{tag}::Configuration Manager object created")

            model_pusher_config = config.get_model_pusher_config()
            logger.info(f"{tag}::Model pusher configuration obtained")

            model_pusher = ModelPusher(config=model_pusher_config)
            logger.info(f"{tag}::Model pusher object created")

            logger.info(f"{tag}::Running the model pusher pipeline")
            model_pusher.push()
            logger.info(f"{tag}::Model pusher pipeline completed")
        except Exception as e:
            logger.error(f"{tag}::Error running the model training pipeline: {e}")
            raise CustomException(e, sys)