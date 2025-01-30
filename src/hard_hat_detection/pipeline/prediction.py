import os
import subprocess
from pathlib import Path


class PredictionPipeline:
    def __init__(self,
                 weights=os.path.join(Path(__file__).parent.parent.parent.parent,
                                      Path('artifacts/model_trainer/results/weights/best.pt')),
                 source=os.path.join(Path(__file__).parent.parent.parent.parent,
                                      Path('detections/predict.jpg')),
                 detect_file= os.path.join(Path(__file__).parent.parent.parent.parent,
                                      Path('yolov5/detect.py')),
                 data_file=os.path.join(Path(__file__).parent.parent.parent.parent,
                                      Path('artifacts/model_trainer/dataset.yaml')),
                 output_folder=os.path.join(Path(__file__).parent.parent.parent.parent,
                                      Path('detections'))):
        self.weights = weights
        self.source = source
        self.detect_file = detect_file
        self.data_file = data_file
        self.output_folder = output_folder
        self.setup_output_folder()

    def get_weights(self):
        return self.weights

    def get_source(self):
        return self.source

    def get_detect_file(self):
        return self.detect_file

    def setup_output_folder(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def run_detection(self):
        if not self.weights:
            raise ValueError('Weights not provided')

        if not self.detect_file:
            raise ValueError('Detect file not provided')

        command = [
            'python', self.detect_file,
            '--weights', self.weights,
            '--source', self.source,
            '--data', self.data_file,
            '--conf', '0.4',
            '--project', self.output_folder,
            '--name', 'results',
            '--exist-ok'
        ]
        subprocess.run(command, check=True)

    def detect_image(self, image_path=None):
        if image_path:
            self.source = image_path

        if not self.source:
            raise ValueError('Image path not provided')
        self.run_detection()

    def detect_video(self, video_path=None):
        if video_path:
            self.source = video_path

        if not self.source:
            raise ValueError('Video path not provided')
        self.run_detection()

    # detect webcam
    def detect_webcam(self):
        self.source = "0"
        self.run_detection()


# Example usage:
if __name__ == "__main__":
    detector = PredictionPipeline()
    weights_path = detector.get_weights()
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f'Weights not found at: {weights_path}')
    else:
        print(f'Weights found at: {weights_path}')

    # Image detection
    input_source = detector.get_source()
    if not os.path.exists(input_source):
        raise FileNotFoundError(f'Image not found at: {input_source}')
    else:
        print(f'Image found at: {input_source}')

    input_detection_file = detector.get_detect_file()
    if not os.path.exists(input_detection_file):
        raise FileNotFoundError(f'Detect file not found at: {input_detection_file}')
    else:
        print(f'Detect file found at: {input_detection_file}')
    detector.detect_image(input_source)

    # webcam detection
    # detector.detect_webcam()

