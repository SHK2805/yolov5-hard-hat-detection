import os
from pathlib import Path

from src.hard_hat_detection.constants.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from src.hard_hat_detection.entity.config_entity import DataIngestionConfig, DataValidationConfig, \
    DataTransformationConfig, ModelTrainerConfig, ModelEvaluationConfig, ModelPusherConfig
from src.hard_hat_detection.logger.logger_config import logger
from src.hard_hat_detection.utils.common import read_yaml, create_directories


class ConfigurationManager:
    def __init__(self, config_file_path: Path = CONFIG_FILE_PATH, params_file_path: Path = PARAMS_FILE_PATH):
        self.class_name = self.__class__.__name__
        self.config_file_path: Path = config_file_path
        self.config = read_yaml(config_file_path)
        # self.params = read_yaml(params_file_path)
        # create the artifacts directory
        self.artifacts_dir = self.config.artifacts_root
        logger.info(f"Artifacts directory: {self.artifacts_dir}")
        create_directories([os.path.join(self.artifacts_dir)])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        tag: str = f"{self.class_name}::get_data_ingestion_config::"
        config = self.config.data_ingestion
        logger.info(f"{tag}Data ingestion configuration obtained from the config file")

        # create the data directory
        data_dir = config.data_root_dir
        logger.info(f"{tag}Data directory: {data_dir} obtained from the config file")

        create_directories([data_dir])
        logger.info(f"{tag}Data directory created: {data_dir}")

        # get roboflow API key
        rf = read_yaml(Path(config.roboflow_api_key_file))
        # check if file exists
        if not rf:
            logger.error(f"{tag}Roboflow API key file {config.roboflow_api_key_file} not read")
            raise FileNotFoundError(f"Roboflow API key file not read")
        roboflow_api_key = rf.roboflow_api_key.ROBOFLOW_API_KEY



        data_ingestion_config: DataIngestionConfig = DataIngestionConfig(
            data_root_dir = Path(config.data_root_dir),
            roboflow_api_key_file = config.roboflow_api_key_file,
            roboflow_api_key = roboflow_api_key,
            roboflow_workspace = config.roboflow_workspace,
            roboflow_project = config.roboflow_project,
            roboflow_version = config.roboflow_version,
            roboflow_export_format = config.roboflow_export_format
        )
        logger.info(f"{tag}Data ingestion configuration created")
        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        tag: str = f"{self.class_name}::get_data_validation_config::"
        config = self.config.data_validation
        logger.info(f"{tag}Data validation configuration obtained from the config file")

        # create the data directory
        data_dir = config.data_root_dir
        logger.info(f"{tag}Data directory: {data_dir} obtained from the config file")

        create_directories([data_dir])
        logger.info(f"{tag}Data directory created: {data_dir}")

        data_validation_config: DataValidationConfig = DataValidationConfig(
            data_root_dir=Path(config.data_root_dir),
            data_dir=Path(config.data_dir),
            STATUS_FILE=config.STATUS_FILE,
            TRAIN_DIR=config.TRAIN_DIR,
            VAL_DIR=config.VAL_DIR,
            TEST_DIR=config.TEST_DIR,
            IMG_DIR=config.IMG_DIR,
            LABEL_DIR=config.LABEL_DIR,
            LABELS_FILE_EXT=config.LABELS_FILE_EXT,
            DATA_FILE=config.DATA_FILE
        )
        logger.info(f"{tag}Data validation configuration created")
        return data_validation_config

    def get_data_transformation_config(self) -> DataTransformationConfig:
        tag: str = f"{self.class_name}::get_data_transformation_config::"
        config = self.config.data_transformation
        logger.info(f"{tag}Data transformation configuration obtained from the config file")

        # create the data directory
        data_dir = config.data_root_dir
        logger.info(f"{tag}Data directory: {data_dir} obtained from the config file")
        create_directories([data_dir])
        logger.info(f"{tag}Data directory created: {data_dir}")

        data_transformation_config: DataTransformationConfig = DataTransformationConfig(
            data_root_dir=Path(config.data_root_dir),
            data_dir=Path(config.data_dir),
            TRAIN_DIR=config.TRAIN_DIR,
            VAL_DIR=config.VAL_DIR,
            TEST_DIR=config.TEST_DIR,
            IMG_DIR=config.IMG_DIR,
            LABEL_DIR=config.LABEL_DIR,
            IMG_FILE_EXT=config.IMG_FILE_EXT,
            LABELS_FILE_EXT=config.LABELS_FILE_EXT
        )
        logger.info(f"{tag}Data transformation configuration created")
        return data_transformation_config

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        tag: str = f"{self.class_name}::get_model_trainer_config::"
        config = self.config.model_trainer
        logger.info(f"{tag}Model training configuration obtained from the config file")

        # create the data directory
        data_dir = config.data_root_dir
        logger.info(f"{tag}Data directory: {data_dir} obtained from the config file")
        create_directories([data_dir])
        logger.info(f"{tag}Data directory created: {data_dir}")

        model_trainer_config: ModelTrainerConfig = ModelTrainerConfig(
            data_root_dir=config.data_root_dir,
            data_dir=config.data_dir,
            input_yaml_path=config.input_yaml_path,
            output_yaml_path=config.output_yaml_path,
            TRAIN_DIR=config.TRAIN_DIR,
            VAL_DIR=config.VAL_DIR,
            TEST_DIR=config.TEST_DIR,
            model_root_path=config.model_root_path,
            used_model_name=config.used_model_name,
            weight_name=config.weight_name,
            no_epochs=config.no_epochs,
            batch_size=config.batch_size
        )
        logger.info(f"{tag}Model training configuration created")
        return model_trainer_config

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        tag: str = f"{self.class_name}::get_model_evaluation_config::"
        config = self.config.model_evaluation
        logger.info(f"{tag}Model evaluation configuration obtained from the config file")

        # create the data directory
        data_dir = config.data_root_dir
        logger.info(f"{tag}Data directory: {data_dir} obtained from the config file")
        # create_directories([data_dir])
        # logger.info(f"{tag}Data directory created: {data_dir}")

        model_evaluation_config: ModelEvaluationConfig = ModelEvaluationConfig(
            data_root_dir=config.data_root_dir,
            data_dir=config.data_dir,
            input_yaml_path=config.input_yaml_path,
            weights_path=config.weights_path,
            model_root_path=config.model_root_path,
            used_model_name=config.used_model_name,
            batch_size=config.batch_size
        )

        return model_evaluation_config

    def get_model_pusher_config(self) -> ModelPusherConfig:
        tag: str = f"{self.class_name}::get_model_pusher_config::"
        config = self.config.model_pusher
        logger.info(f"{tag}Model pusher configuration obtained from the config file")

        model_pusher_config: ModelPusherConfig = ModelPusherConfig(
            s3_bucket_name = config.s3_bucket_name,
            region_name = config.region_name,
            # model
            weights_path = config.weights_path,
            dataset_yaml_path = config.dataset_yaml_path
        )

        return model_pusher_config



