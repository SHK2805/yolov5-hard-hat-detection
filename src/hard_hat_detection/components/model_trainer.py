import os
import subprocess
import sys
from pathlib import Path

from src.hard_hat_detection.entity.config_entity import ModelTrainerConfig
from src.hard_hat_detection.exception.exception import CustomException
from src.hard_hat_detection.logger.logger_config import logger
from src.hard_hat_detection.utils.common import copy_file
from src.hard_hat_detection.utils.dataset_yaml_generator import DatasetYamlGenerator


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.class_name = self.__class__.__name__
        self.config = config
        self.project_root_path = Path(__file__).parent.parent.parent.parent

    def generate_dataset_yaml(self):
        tag: str = f"{self.class_name}::generate_dataset_yaml::"
        try:
            logger.info(f"{tag}::Generating the dataset yaml file")
            data = {
                'path': str(os.path.join("..", self.config.data_dir)),
                'train': self.config.TRAIN_DIR,
                'val': self.config.VAL_DIR,
                'test': self.config.TEST_DIR
            }
            dataset_yaml_generator = DatasetYamlGenerator(
                input_yaml_path=self.config.input_yaml_path,
                output_yaml_path=self.config.output_yaml_path,
                data=data
            )
            dataset_yaml_generator.run()
            logger.info(f"{tag}Generated the dataset yaml: {self.config.output_yaml_path}")
        except Exception as e:
            logger.error(f"{tag}::Error generating the dataset yaml file: {e}")
            raise e

    def check_yolo_v5(self):
        tag: str = f"{self.class_name}::check_yolo_v5::"
        try:
            logger.info(f"{tag}::Checking the yolov5 repository")

            yolo_path = os.path.join(self.project_root_path, self.config.model_root_path)
            logger.info(f"{tag}::Checking the yolov5 repository at: {yolo_path}")

            if os.path.exists(yolo_path):
                logger.info(f"{tag}::yolov5 repository already exists at: {yolo_path}")
                return True
            else:
                logger.error(f"{tag}::The yolov5 repository does not exist at: {yolo_path}")
                return False
        except Exception as e:
            logger.error(f"{tag}::Error checking the yolov5 repository: {e}")
            raise e

    def get_train_script_path(self):
        tag: str = f"{self.class_name}::get_train_script_path::"
        train_script_path = os.path.join(self.config.model_root_path, "train.py")
        if not os.path.exists(train_script_path):
            raise FileNotFoundError(f"File {train_script_path} does not exist")
        return train_script_path

    def construct_command(self, train_script_path, data_yaml_path):
        results_path = os.path.join(self.project_root_path, self.config.data_root_dir)
        additional_args = (f"--weights {self.config.weight_name} "
                           f"--data {data_yaml_path} "
                           f"--batch {self.config.batch_size} "
                           f"--epochs {self.config.no_epochs}  "
                           f"--exist-ok "
                           f"--name results  "
                           f"--project {results_path} "
                           f"--cache")
        # TODO: Write the yolo console logs to a file in the logs directory or model_trainer directory
        return f'python {train_script_path} {additional_args}'

    def run_training(self, command):
        tag: str = f"{self.class_name}::run_training::"
        try:
            logger.info(f"{tag}::Running the training command")
            # Uncomment the line below to execute the command
            subprocess.run(command, shell=True)
        except Exception as e:
            logger.error(f"{tag}::Error running the training command: {e}")
            raise e

    def copy_weights(self):
        tag: str = f"{self.class_name}::copy_weights::"
        weights_source_path = os.path.join(self.project_root_path, self.config.weight_name)
        weights_destination_path = os.path.join(self.project_root_path, self.config.data_root_dir)
        if os.path.exists(weights_source_path):
            copy_file(weights_source_path, weights_destination_path)
            logger.info(f"{tag}::Weights file copied from {weights_source_path} to {weights_destination_path}")
        else:
            logger.error(f"{tag}::Weights file does not exist at {weights_source_path}")
            raise FileNotFoundError(f"File {weights_source_path} does not exist")

    def train(self):
        tag: str = f"{self.class_name}::train::"
        try:
            logger.info(f"{tag}::Training the model")
            self.generate_dataset_yaml()
            data_yaml_path = self.config.output_yaml_path
            if not os.path.exists(data_yaml_path):
                logger.error(f"File {data_yaml_path} does not exist")
                raise FileNotFoundError(f"File {data_yaml_path} does not exist")

            if not self.check_yolo_v5():
                logger.error(f"YOLO repository does not exist")
                raise FileNotFoundError(f"YOLO repository does not exist")

            train_script_path = self.get_train_script_path()
            command = self.construct_command(train_script_path, data_yaml_path)
            logger.info(f"{tag}::Command to train the model: {command}")

            self.run_training(command)
            self.copy_weights()
            logger.info(f"{tag}::Model training completed")
        except Exception as e:
            logger.error(f"{tag}::Error training the model: {e}")
            raise CustomException(e, sys)
