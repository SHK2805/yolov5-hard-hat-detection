import os
import shutil
import sys
from pathlib import Path

import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations

from src.hard_hat_detection.exception.exception import CustomException
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
        raise CustomException(e, sys)

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

# function to get environment variables
def get_env_var(env_var: str) -> str:
    """
    Get the environment variable

    :param env_var: Environment variable
    :return: Value of the environment variable
    """
    # check if the environment variable exists
    if env_var not in os.environ:
        raise ValueError(f"Environment variable: {env_var} does not exist")
    return os.environ[env_var]

# check if a directory exists and is not empty
def check_directory_not_empty(directory: Path) -> bool:
    """
    Check if the directory exists and is not empty

    :param directory: Path to the directory
    :return: True if the directory exists and is not empty, False otherwise
    """
    return directory.exists() and any(directory.iterdir())

# get project root path
def get_project_root_path():
    """
    Get the project root path

    :return: Project root path
    """
    return sys.path[1]

def check_paths(base_directory, paths_to_check):
    all_present = True
    for path in paths_to_check:
        if not os.path.exists(os.path.join(base_directory, path)):
            logger.warning(f"Path {os.path.join(base_directory, path)} does not exist")
            all_present = False
    return all_present


def copy_folder(source_path: str, destination_path: str):
    shutil.copytree(source_path, destination_path, dirs_exist_ok=True)

def copy_file(source_path: str, destination_path: str):
    shutil.copy2(source_path, destination_path)

def delete_if_exists(path):
    if os.path.exists(path):
        # If it's a directory, remove it and all its contents
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            # If it's a file, remove it
            os.remove(path)
        logger.info(f"{path} has been deleted.")
    else:
        logger.warning(f"{path} does not exist.")
