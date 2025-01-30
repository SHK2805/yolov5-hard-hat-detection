import os
import subprocess
import sys
from pathlib import Path

from src.hard_hat_detection.entity.config_entity import ModelEvaluationConfig
from src.hard_hat_detection.exception.exception import CustomException
from src.hard_hat_detection.logger.logger_config import logger


class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.class_name = self.__class__.__name__
        self.config = config
        self.project_root_path = Path(__file__).parent.parent.parent.parent

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

    def get_val_script_path(self):
        tag: str = f"{self.class_name}::get_val_script_path::"
        vla_script_path = os.path.join(self.config.model_root_path, "val.py")
        if not os.path.exists(vla_script_path):
            logger.error(f"File {vla_script_path} does not exist")
            raise FileNotFoundError(f"File {vla_script_path} does not exist")
        return vla_script_path

    def construct_command(self, val_script_path, data_yaml_path):
        results_path = os.path.join(self.project_root_path, self.config.data_root_dir)
        additional_args = (f"--weights {self.config.weights_path} "
                           f"--data {data_yaml_path} "
                           f"--batch {self.config.batch_size} "
                           f"--exist-ok "
                           f"--name results  "
                           f"--project {results_path}")
        # TODO: Write the yolo console logs to a file in the logs directory or model_evaluation directory
        return f'python {val_script_path} {additional_args}'

    def run_evaluation(self, command):
        tag: str = f"{self.class_name}::run_evaluation::"
        try:
            logger.info(f"{tag}::Running the evaluation command")
            # Uncomment the line below to execute the command
            subprocess.run(command, shell=True)
        except Exception as e:
            logger.error(f"{tag}::Error running the evaluation command: {e}")
            raise e

    def evaluate(self):
        tag: str = f"{self.class_name}::evaluate::"
        try:
            data_yaml_path = self.config.input_yaml_path
            if not os.path.exists(data_yaml_path):
                logger.error(f"File {data_yaml_path} does not exist")
                raise FileNotFoundError(f"File {data_yaml_path} does not exist")

            if not self.check_yolo_v5():
                raise FileNotFoundError(f"YOLO repository does not exist")

            val_script_path = self.get_val_script_path()
            if not os.path.exists(val_script_path):
                raise FileNotFoundError(f"File {val_script_path} does not exist")
            command = self.construct_command(val_script_path, data_yaml_path)
            logger.info(f"{tag}::Command to evaluate the model: {command}")

            self.run_evaluation(command)
            logger.info(f"{tag}::Model evaluation completed")

        except Exception as e:
            logger.error(f"{tag}Error evaluating the data: {e}")
            raise CustomException(e, sys)