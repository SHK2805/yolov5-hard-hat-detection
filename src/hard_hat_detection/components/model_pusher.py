import sys
from pathlib import Path

from cloud.deploy import bucket_name
from src.hard_hat_detection.entity.config_entity import ModelPusherConfig
from src.hard_hat_detection.exception.exception import CustomException
from src.hard_hat_detection.logger.logger_config import logger
from src.hard_hat_detection.utils.s3_operations import S3Operations


class ModelPusher:
    def __init__(self,config: ModelPusherConfig):
        self.class_name = self.__class__.__name__
        self.config: ModelPusherConfig = config
        self.project_root_path = Path(__file__).parent.parent.parent.parent

    # There is a limit to the number of times you can download data from Roboflow.
    # If you have already downloaded the data, you can skip this step.
    def push(self):
        tag: str = f"{self.class_name}::push::"
        try:
            # pushing the model to cloud s3
            logger.info(f"{tag}Pushing model to s3")

            s3_client = S3Operations(bucket_name=self.config.s3_bucket_name,
                                     region_name=self.config.region_name)

            # check if bucket exists
            if not s3_client.bucket_exists():
                raise FileNotFoundError(f"{tag}Bucket {self.config.s3_bucket_name} not found")

            # check if the files exist
            if not Path(self.config.weights_path).exists():
                raise FileNotFoundError(f"{tag}Weights file {self.config.weights_path} not found")

            if not Path(self.config.dataset_yaml_path).exists():
                raise FileNotFoundError(f"{tag}Dataset yaml file {self.config.dataset_yaml_path} not found")

            s3_client.upload_file(file_name=self.config.weights_path)
            s3_client.upload_file(file_name=self.config.dataset_yaml_path)


        except Exception as e:
            logger.error(f"{tag}Error in pushing model: {e}")
            raise CustomException(e, sys)



