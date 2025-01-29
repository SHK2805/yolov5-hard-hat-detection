import os.path
from pathlib import Path
from src.hard_hat_detection.utils.delete_directories import delete_directories


def clean():
    try:
        # paths = [Path("logs")]
        # paths = [Path("artifacts"), Path("logs")]
        # paths = [Path("artifacts"), Path("logs"), Path("yolov5")]
        paths = [Path("artifacts/data_transformation"), Path("artifacts/data_validation"), Path("artifacts/model_trainer"), Path("logs")]
        # delete the folders
        delete_directories(paths)
        print(f"Cleaned up the project directories")

        if os.path.exists("yolov5s.pt"):
            # os.remove("yolov5s.pt")
            print(f"Removed the yolov5s.pt file")

    except Exception as e:
        raise e

if __name__ == "__main__":
    clean()