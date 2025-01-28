import os
import subprocess
from src.hard_hat_detection.entity.config_entity import ModelTrainerConfig
from src.hard_hat_detection.logger.logger_config import logger
from src.hard_hat_detection.utils.dataset_yaml_generator import DatasetYamlGenerator


class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.class_name = self.__class__.__name__
        self.config = config

    def train(self):
        tag: str = f"{self.class_name}::train::"
        try:
            logger.info(f"{tag}::Training the model")
            # generate the dataset yaml
            data = {
                'path': str(self.config.data_dir),
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

            data_yaml_path = self.config.output_yaml_path
            if not os.path.exists(data_yaml_path):
                raise FileNotFoundError(f"File {data_yaml_path} does not exist")


            # train the model
            # Define the path to the training script
            train_script_path = os.path.join(self.config.model_root_path, "train.py")
            if not os.path.exists(train_script_path):
                raise FileNotFoundError(f"File {train_script_path} does not exist")

            # Define the command to train the model
            # Optional: Define any additional arguments
            # For example: --img 640 --batch 16 --epochs 50 --data coco.yaml --weights yolov5s.pt
            results_path = os.path.join(self.config.data_root_dir, "results")
            additional_args = (f"--weights {self.config.weight_name} "
                               f"--data {data_yaml_path} "
                               f"--batch {self.config.batch_size} "
                               f"--epochs {self.config.no_epochs}  "
                               f"--name {results_path}  "
                               f"--cache")

            # Construct the command
            command = f'python {train_script_path} {additional_args}'

            # Execute the command
            subprocess.run(command, shell=True)

            logger.info(f"{tag}::Model training completed")
        except Exception as e:
            logger.error(f"{tag}::Error training the model: {e}")
            raise e