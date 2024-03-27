import os
import logging
import re
import yaml


class Utils():

    logger = logging.getLogger(__name__)

    @staticmethod
    def create_dir(directory_path: str) -> None:
        os.makedirs(directory_path)

    @staticmethod
    def load_config(config_file: str) -> dict:
        Utils.logger.info('Loading workflow')
        with open(config_file, 'r') as f:
            data = yaml.safe_load(f)
        return data

    @staticmethod
    def save_config(config_data: dict, file_path: str) -> None:
        with open(file_path, 'w') as f:
            yaml.safe_dump(
                config_data, f, default_flow_style=False, sort_keys=False)

    @staticmethod
    def convert_to_module_name(class_name: str) -> str:
        module_name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()
        return module_name

    @staticmethod
    def combine_parameters(global_parameters: dict, node_parameters: dict) -> dict:
        # If either dictionary is empty, return the other one
        if not global_parameters:
            return node_parameters
        if not node_parameters:
            return global_parameters
        
        # If both dictionaries have entries, combine them
        combined_parameters = node_parameters.copy()
        for parameter, value in global_parameters.items():
            if parameter not in combined_parameters:
                combined_parameters[parameter] = value
        return combined_parameters
