import yaml

from src.hard_hat_detection.logger.logger_config import logger


class DatasetYamlGenerator:
    def __init__(self, input_yaml_path, output_yaml_path, data):
        self.input_yaml_path = input_yaml_path
        self.output_yaml_path = output_yaml_path
        self.data = data

    def read_names_from_yaml(self):
        with open(self.input_yaml_path, 'r') as file:
            input_data = yaml.safe_load(file)
        names = input_data.get('names', [])
        self.data['names'] = {i: name for i, name in enumerate(names)}

    def generate_yaml(self):
        with open(self.output_yaml_path, 'w') as file:
            # Write main data first
            for key, value in self.data.items():
                if key != 'names':
                    file.write(f"{key}: {value}\n")
            # Write names last
            file.write('\nnames:\n')
            for idx, name in self.data['names'].items():
                file.write(f"    {idx}: {name}\n")
        logger.info(f"YAML file has been generated at {self.output_yaml_path}")

    def run(self):
        self.read_names_from_yaml()
        self.generate_yaml()
