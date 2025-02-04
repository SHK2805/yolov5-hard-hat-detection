import sys
from datetime import datetime

import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

from src.hard_hat_detection.exception.exception import CustomException
from src.hard_hat_detection.logger.logger_config import logger


class S3Operations:
    def __init__(self, bucket_name = 'shks3yolov5cvlive', region_name='us-east-1'):
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3', region_name=region_name)
        self.s3_resource = boto3.resource('s3', region_name=region_name)

    def bucket_exists(self):
        try:
            self.s3.head_bucket(Bucket=self.bucket_name)
            return True
        except ClientError:
            return False

    def create_bucket(self):
        if not self.bucket_exists():
            try:
                self.s3.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.s3.meta.region_name}
                )
                print(f"Bucket {self.bucket_name} created successfully.")
            except ClientError as e:
                logger.error(f"An error occurred: {e}")
                raise CustomException(e,sys)
        else:
            logger.info(f"Bucket {self.bucket_name} already exists.")

    def upload_file(self, file_name, object_name=None):
        if object_name is None:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            object_name = f"{file_name.rsplit('.', 1)[0]}_{timestamp}.{file_name.rsplit('.', 1)[1]}"

        self.create_bucket()  # Ensure bucket exists before uploading

        try:
            self.s3.upload_file(file_name, self.bucket_name, object_name)
            logger.info(f"File {file_name} uploaded to {self.bucket_name}/{object_name} successfully.")
        except FileNotFoundError as e:
            logger.error(f"The file {file_name} was not found.")
            raise CustomException(e, sys)
        except NoCredentialsError as e:
            logger.error("Credentials not available.")
            raise CustomException(e, sys)
        except PartialCredentialsError as e:
            logger.error("Incomplete credentials provided.")
            raise CustomException(e, sys)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise CustomException(e, sys)

    def download_file(self, object_name, file_name=None):
        if file_name is None:
            file_name = object_name

        if not self.bucket_exists():
            print(f"The bucket {self.bucket_name} does not exist.")
            return

        try:
            self.s3.download_file(self.bucket_name, object_name, file_name)
            print(f"File {object_name} downloaded from {self.bucket_name} to {file_name} successfully.")
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                logger.error(f"The file {object_name} does not exist in the bucket.")
            else:
                logger.error(f"An error occurred: {e}")
            raise CustomException(e, sys)
        except NoCredentialsError as e:
            logger.error("Credentials not available.")
            raise CustomException(e, sys)
        except PartialCredentialsError as e:
            logger.error("Incomplete credentials provided.")
            raise CustomException(e, sys)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise CustomException(e, sys)


# Example usage:
if __name__ == "__main__":
    s3_ops = S3Operations()
    s3_ops.upload_file('best.pt')
    s3_ops.download_file('best.pt')
