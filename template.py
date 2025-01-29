import os
from pathlib import Path
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')


def create_directory(path: Path):
    if not path.exists():
        os.makedirs(path, exist_ok=True)
        logging.info(f"Creating directory: {path}")
    else:
        logging.info(f"Directory {path} already exists")


def create_file(filepath: Path):
    if not filepath.exists() or filepath.stat().st_size == 0:
        filepath.touch()
        logging.info(f"Creating empty file: {filepath}")
    else:
        logging.info(f"{filepath.name} already exists")


def create_project_structure(project_name: str) -> bool:
    try:
        list_of_files = [
            # general files
            "template.py",
            ".gitignore",
            ".dockerignore",
            "docker-compose.yml",
            "deploy.py",
            "cloudformation_template.yaml",
            "requirements.txt",
            "README.md",
            "Dockerfile",
            # log files
            f"logs/log_{project_name}.log",
            f"src/__init__.py",
            f"src/{project_name}/__init__.py",
            # components
            f"src/{project_name}/components/__init__.py",
            f"src/{project_name}/components/data_cleaning.py",
            f"src/{project_name}/components/data_ingestion.py",
            f"src/{project_name}/components/data_validation.py",
            f"src/{project_name}/components/data_transformation.py",
            f"src/{project_name}/components/model_trainer.py",
            f"src/{project_name}/components/model_evaluation.py",
            # logger
            f"src/{project_name}/logger/__init__.py",
            f"src/{project_name}/logger/logger_config.py",
            # utils
            f"src/{project_name}/utils/__init__.py",
            f"src/{project_name}/utils/common.py",
            f"src/{project_name}/utils/delete_directories.py",
            # config
            f"src/{project_name}/config/__init__.py",
            f"src/{project_name}/config/configuration.py",
            # pipeline
            f"src/{project_name}/pipeline/__init__.py",
            f"src/{project_name}/pipeline/data_ingestion.py",
            f"src/{project_name}/pipeline/data_validation.py",
            f"src/{project_name}/pipeline/data_transformation.py",
            f"src/{project_name}/pipeline/model_trainer.py",
            f"src/{project_name}/pipeline/model_evaluation.py",
            f"src/{project_name}/pipeline/prediction.py",
            # entity
            f"src/{project_name}/entity/__init__.py",
            f"src/{project_name}/entity/config_entity.py",
            # constants
            f"src/{project_name}/constants/__init__.py",
            f"src/{project_name}/constants/constants.py",
            # config, params, schema
            "config/config.yaml",
            "params.yaml",
            # research
            "research/research.py",
            # other files
            "main.py",
            "setup.py",
            # app
            "templates/index.html",
            "templates/error.html",
            "app.py",
            # clean
            "clean.py"
        ]

        for filepath in list_of_files:
            filepath = Path(filepath)
            filedir = filepath.parent

            # Ensure Dockerfile, docker-compose.yml and .dockerignore are treated as files
            if filepath.name in ['Dockerfile', '.dockerignore', 'docker-compose.yml', 'deploy.py', 'cloudformation_template.yaml']:
                create_file(filepath)
                continue

            # Create directories
            create_directory(filedir)

            # Create files if they do not exist or are empty
            if filepath.suffix:  # Check if it's a file (has a suffix)
                create_file(filepath)
            else:
                create_directory(filepath)
    except Exception as e:
        logging.error(f"Error in creating project structure: {e}")
        return False
    return True


if __name__ == "__main__":
    cv_project_name = "hard_hat_detection"
    create_project_structure(cv_project_name)
    logging.info(f"Project structure created for {cv_project_name}")
