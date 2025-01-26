from pathlib import Path

from src.hard_hat_detection.utils.common import read_yaml


def get_roboflow_api_key():
    rf = read_yaml(Path("../roboflow_api_key.yaml"))
    # check if file exists
    if rf:
        return rf.roboflow_api_key.ROBOFLOW_API_KEY
    else:
        return "None"

if __name__ == "__main__":
    print(get_roboflow_api_key())