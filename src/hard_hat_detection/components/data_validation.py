import os.path
from pathlib import Path

from src.hard_hat_detection.entity.config_entity import DataValidationConfig
from src.hard_hat_detection.logger.logger_config import logger
from src.hard_hat_detection.utils.common import write_data_to_file

"""
check if the downloaded data for a computer vision project is correct. 
The downloaded data is of the below format 
The root folder is data_ingestion under this folder there are three folders test, train and valid folders and a data.yaml file. 
Under the test train and valid folders each of them have images and labels folders 
inside the images folder there are images and for each image there is a corresponding .txt file in labels folder. 
The images and labels folders should not be empty and there should be files corresponding to each other. 
This class validates the below
    The folder structure exists and that the images and label folders are not empty
    For each image in images folder there is a corresponding label .txt file.
    The data.yaml file exists
"""

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.class_name = self.__class__.__name__
        self.config = config
        self.data_dir = config.data_dir
        self.required_folders = [config.TEST_DIR, config.TRAIN_DIR, config.VAL_DIR]
        self.image_folder = config.IMG_DIR
        self.label_folder = config.LABEL_DIR

    def validate_folder_structure(self):
        tag: str = f"{self.class_name}::validate_folder_structure::"
        try:
            if not os.path.exists(self.data_dir):
                logger.info(f"{tag}Data directory {self.data_dir} does not exist")
                return False
            for folder in self.required_folders:
                folder_path = os.path.join(self.data_dir, folder)
                if not os.path.exists(folder_path):
                    logger.info(f"{tag}Missing folder: {folder_path}")
                    return False
                if not os.path.exists(os.path.join(folder_path, self.image_folder)):
                    logger.info(f"{tag}Missing {self.image_folder} folder in {folder}")
                    return False
                if not os.path.exists(os.path.join(folder_path, self.label_folder)):
                    logger.info(f"{tag}Missing {self.label_folder} folder in {folder}")
                    return False
            return True
        except Exception as e:
            logger.error(f"{tag}Error reading the data: {e}")
            return False

    def validate_files(self, folder_path):
        tag: str = f"{self.class_name}::validate_files::"
        try:
            image_files = os.listdir(os.path.join(folder_path, self.image_folder))
            label_files = os.listdir(os.path.join(folder_path, self.label_folder))

            if not image_files:
                logger.info(f"{tag}No images found in {folder_path}")
                return False
            if not label_files:
                logger.info(f"{tag}No labels found in {folder_path}")
                return False

            for image_file in image_files:
                label_file = os.path.splitext(image_file)[0] + '.txt'
                if label_file not in label_files:
                    logger.info(f"{tag}Missing label file for {image_file} in {folder_path}")
                    return False

            return True
        except Exception as e:
            logger.error(f"{tag}Error reading the data: {e}")
            return False

    def validate_data(self):
        tag: str = f"{self.class_name}::validate_data::"
        try:
            if not self.validate_folder_structure():
                logger.info(f"{tag}Validation failed for folder structure")
                return False

            for folder in self.required_folders:
                folder_path = os.path.join(self.data_dir, folder)
                if not self.validate_files(folder_path):
                    logger.info(f"{tag}Validation failed for files in {folder_path}")
                    return False

            # check data.yaml file
            if not os.path.exists(os.path.join(self.data_dir, 'data.yaml')):
                logger.info(f"{tag}Missing data.yaml file in {self.data_dir}")
                return False

            return True
        except Exception as e:
            logger.error(f"{tag}Error reading the data: {e}")
            return False


    def validate(self):
        tag: str = f"{self.class_name}::validate::"
        validation_status = self.validate_data()
        status_file = Path(os.path.join(self.config.STATUS_FILE))
        write_data_to_file(status_file, str(validation_status))
        logger.info(f"{tag}Validation status {str(validation_status)} written to file: {status_file}")
        return validation_status
