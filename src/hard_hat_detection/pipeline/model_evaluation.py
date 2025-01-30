from src.hard_hat_detection.components.model_evaluation import ModelEvaluation
from src.hard_hat_detection.config.configuration import ConfigurationManager
from src.hard_hat_detection.logger.logger_config import logger

STAGE_NAME: str = "Model Evaluation Pipeline"
class ModelEvaluationTrainingPipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__
        self.stage_name = STAGE_NAME

    def model_evaluation(self) -> None:
        tag: str = f"{self.class_name}::model_evaluation::"
        try:
            config = ConfigurationManager()
            logger.info(f"{tag}::Configuration Manager object created")

            model_evaluation_config = config.get_model_evaluation_config()
            logger.info(f"{tag}::Model evaluation configuration obtained")

            model_eval = ModelEvaluation(config=model_evaluation_config)
            logger.info(f"{tag}::Model evaluation object created")

            logger.info(f"{tag}::Running the model evaluation pipeline")
            model_eval.evaluate()
            logger.info(f"{tag}::Model evaluation pipeline completed")
        except Exception as e:
            logger.error(f"{tag}::Error running the model evaluation pipeline: {e}")
            raise e