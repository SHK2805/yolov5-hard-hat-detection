import os.path
from pathlib import Path
from src.hard_hat_detection.utils.delete_directories import delete_directories


def clean():
    try:
        # paths = [Path("logs")]
        paths = [Path("artifacts"), Path("logs")]
        # paths = [Path("artifacts"), Path("logs"), Path("yolov5")]
        # paths = [Path("artifacts/data_transformation"), Path("artifacts/data_validation"), Path("artifacts/model_trainer"), Path("logs")]
        # delete the folders
        delete_directories(paths)
        print(f"Cleaned up the project directories")

        # delete the files
        file_name: str = "yolov5s.pt"
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"Removed the {file_name} file")

    except Exception as e:
        raise e

if __name__ == "__main__":
    clean()