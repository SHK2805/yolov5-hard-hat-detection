import sys

from src.hard_hat_detection.exception.exception import CustomException
from src.hard_hat_detection.logger.logger_config import logger
from src.hard_hat_detection.pipeline.data_ingestion import DataIngestionTrainingPipeline
from src.hard_hat_detection.pipeline.data_validation import DataValidationTrainingPipeline
from src.hard_hat_detection.pipeline.data_transformation import DataTransformationTrainingPipeline
from src.hard_hat_detection.pipeline.model_trainer import ModelTrainerTrainingPipeline


class RunPipeline:
    def __init__(self):
        self.class_name = self.__class__.__name__
        self.data_ingestion_pipeline: DataIngestionTrainingPipeline = DataIngestionTrainingPipeline()
        self.data_validation_pipeline: DataValidationTrainingPipeline = DataValidationTrainingPipeline()
        self.data_transformation_pipeline: DataTransformationTrainingPipeline = DataTransformationTrainingPipeline()
        self.model_trainer_pipeline: ModelTrainerTrainingPipeline = ModelTrainerTrainingPipeline()

    def run_data_ingestion_pipeline(self) -> None:
        tag: str = f"{self.class_name}::run_data_ingestion_pipeline::"
        try:
            logger.info(f"[STARTED]>>>>>>>>>>>>>>>>>>>> {self.data_ingestion_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<")
            logger.info(f"{tag}::Running the data ingestion pipeline")
            self.data_ingestion_pipeline.data_ingestion()
            logger.info(f"{tag}::Data ingestion pipeline completed")
            logger.info(
                f"[COMPLETE]>>>>>>>>>>>>>>>>>>>> {self.data_ingestion_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<\n\n\n")
        except Exception as e:
            logger.error(f"{tag}::Error running the data ingestion pipeline: {e}")
            raise CustomException(e, sys)

    def run_data_validation_pipeline(self) -> None:
        tag: str = f"{self.class_name}::run_data_validation_pipeline::"
        try:
            logger.info(
                f"[STARTED]>>>>>>>>>>>>>>>>>>>> {self.data_validation_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<")
            logger.info(f"{tag}::Running the data validation pipeline")
            self.data_validation_pipeline.data_validation()
            logger.info(f"{tag}::Data validation pipeline completed")
            logger.info(
                f"[COMPLETE]>>>>>>>>>>>>>>>>>>>> {self.data_validation_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<\n\n\n")
        except Exception as e:
            logger.error(f"{tag}::Error running the data validation pipeline: {e}")
            raise CustomException(e, sys)

    def run_data_transformation_pipeline(self) -> None:
        tag: str = f"{self.class_name}::run_data_transformation_pipeline::"
        try:
            logger.info(
                f"[STARTED]>>>>>>>>>>>>>>>>>>>> {self.data_transformation_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<")
            logger.info(f"{tag}::Running the data transformation pipeline")
            # self.train_loader, self.val_loader, self.test_loader = self.data_transformation_pipeline.data_transformation()
            self.data_transformation_pipeline.data_transformation()
            logger.info(f"{tag}::Data transformation pipeline completed")
            logger.info(
                f"[COMPLETE]>>>>>>>>>>>>>>>>>>>> {self.data_transformation_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<\n\n\n")
        except Exception as e:
            logger.error(f"{tag}::Error running the data transformation pipeline: {e}")
            raise CustomException(e, sys)

    def run_model_trainer_pipeline(self) -> None:
        tag: str = f"{self.class_name}::run_model_training_pipeline::"
        try:
            logger.info(f"[STARTED]>>>>>>>>>>>>>>>>>>>> {self.model_trainer_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<")
            logger.info(f"{tag}::Running the model training pipeline")
            self.model_trainer_pipeline.model_trainer()
            logger.info(f"{tag}::Model training pipeline completed")
            logger.info(
                f"[COMPLETE]>>>>>>>>>>>>>>>>>>>> {self.model_trainer_pipeline.stage_name} <<<<<<<<<<<<<<<<<<<<\n\n\n")
        except Exception as e:
            logger.error(f"{tag}::Error running the model training pipeline: {e}")
            raise CustomException(e, sys)


    def run(self) -> None:
        self.run_data_ingestion_pipeline()
        self.run_data_validation_pipeline()
        self.run_data_transformation_pipeline()
        self.run_model_trainer_pipeline()

if __name__ == "__main__":
    # Run the pipelines
    run_pipeline = RunPipeline()
    run_pipeline.run()