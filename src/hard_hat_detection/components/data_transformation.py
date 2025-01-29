import os
import shutil
import sys

from src.hard_hat_detection.entity.config_entity import DataTransformationConfig
from src.hard_hat_detection.exception.exception import CustomException
from src.hard_hat_detection.logger.logger_config import logger


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.class_name = self.__class__.__name__
        self.config = config
        self.old_root = config.data_dir
        self.new_root = config.data_root_dir
        self.old_folders = [config.TRAIN_DIR, config.TEST_DIR, config.VAL_DIR]
        self.new_folders = [config.IMG_DIR, config.LABEL_DIR]

        # Create the new folder structure
        self.create_new_folder_structure()

    def create_new_folder_structure(self):
        tag: str = f"{self.class_name}::create_new_folder_structure::"
        for new_folder in self.new_folders:
            os.makedirs(os.path.join(self.new_root, new_folder), exist_ok=True)
            for old_folder in self.old_folders:
                os.makedirs(os.path.join(self.new_root, new_folder, old_folder), exist_ok=True)

    def copy_files(self, src_folder, dest_folder, file_extension):
        tag: str = f"{self.class_name}::copy_files::"
        for old_folder in self.old_folders:
            src_path = os.path.join(self.old_root, old_folder, src_folder)
            dest_path = os.path.join(self.new_root, dest_folder, old_folder)
            for file_name in os.listdir(src_path):
                if file_name.endswith(file_extension):
                    src_file = os.path.join(src_path, file_name)
                    dest_file = os.path.join(dest_path, file_name)
                    shutil.copy(src_file, dest_file)

    def transform_data(self):
        tag: str = f"{self.class_name}::transform_data::"
        # Copy images and labels
        self.copy_files(self.config.IMG_DIR, self.config.IMG_DIR, self.config.IMG_FILE_EXT)
        self.copy_files(self.config.LABEL_DIR, self.config.LABEL_DIR, self.config.LABELS_FILE_EXT)
        logger.info(f"{tag}Files have been copied successfully!")

    def validate_data(self):
        tag: str = f"{self.class_name}::validate_data::"
        for old_folder in self.old_folders:
            images_path = os.path.join(self.new_root, self.config.IMG_DIR, old_folder)
            labels_path = os.path.join(self.new_root, self.config.LABEL_DIR, old_folder)
            images = {os.path.splitext(img)[0] for img in os.listdir(images_path) if img.endswith(self.config.IMG_FILE_EXT)}
            labels = {os.path.splitext(lbl)[0] for lbl in os.listdir(labels_path) if lbl.endswith(self.config.LABELS_FILE_EXT)}

            missing_labels = images - labels
            missing_images = labels - images

            if missing_labels:
                logger.info(f"{tag}Missing labels for images in {old_folder}: {missing_labels}")
            if missing_images:
                logger.info(f"{tag}Missing images for labels in {old_folder}: {missing_images}")

            if not missing_labels and not missing_images:
                logger.info(f"{tag}All images and labels are matched in {old_folder}")
                return True
            else:
                logger.error(f"{tag}Images and labels are not matched in {old_folder}")
                return False


    def transform(self):
        tag: str = f"{self.class_name}::transform::"
        try:
            self.transform_data()
            validate_data = self.validate_data()
            if not validate_data:
                raise Exception(f"{tag}Data validation failed!")
        except Exception as e:
            logger.error(f"{tag}Error transforming the data: {e}")
            raise CustomException(e, sys)