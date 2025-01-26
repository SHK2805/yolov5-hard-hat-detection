import os
from pathlib import Path

import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations

from src.hard_hat_detection.logger.logger_config import logger


@ensure_annotations
def read_yaml(file_path: Path) -> ConfigBox:
    """
    Read the YAML file and return the ConfigBox object
    ConfigBox:
    ConfigBox is a powerful tool that simplifies configuration management in Python projects.
    By centralizing, organizing, and providing easy access to your configuration settings,
    ConfigBox helps you build more maintainable and flexible applications


    :param file_path: Path to the YAML file
    :return: ConfigBox object
    """
    try:
        with open(file_path, "r") as file:
            config = yaml.safe_load(file)
            logger.info(f"The YAML file: {file_path} has been read successfully")
            return ConfigBox(config)
    except BoxValueError as e:
        logger.error(f"Error reading the YAML file: {e}")
        raise ValueError(f"Error reading the YAML file: {e}")
    except Exception as e:
        logger.error(f"Error reading the YAML file: {e}")
        raise e

def create_directories(dirs: list, verbose=True) -> None:
    """
    Create directories if they do not exist

    :param verbose:
    :param dirs: List of directories to create
    :return: None
    """
    logger.info(f"Creating directories: {dirs}")
    for my_dir in dirs:
        if not os.path.exists(my_dir):
            os.makedirs(my_dir, exist_ok=True)
            if verbose:
                logger.info(f"Directory: {my_dir} has been created")
        else:
            if verbose:
                logger.info(f"Directory: {my_dir} already exists")
    logger.info(f"Directories have been created")

# function to check if the file exists
def check_file_exists(file_path: Path) -> bool:
    """
    Check if the file exists

    :param file_path: Path to the file
    :return: True if the file exists, False otherwise
    """
    return file_path.exists()

# function to write the data to the file
def write_data_to_file(file_path: Path, data: str) -> None:
    """
    Write the data to the file

    :param file_path: Path to the file
    :param data: Data to write
    :return: None
    """
    with open(file_path, "w") as file:
        file.write(data)

    logger.info(f"Data has been written to the file: {file_path}")
