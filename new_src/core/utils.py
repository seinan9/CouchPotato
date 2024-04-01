import os
import re
import yaml


def load_config(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    return data


def save_config(config: dict, file_path: str) -> None:
    with open(file_path, 'w') as f:
        yaml.safe_dump(
            config, f, default_flow_style=False, sort_keys=False)


def create_dir(directory_path: str) -> None:
    os.makedirs(directory_path)


def join_paths(*paths: str) -> str:
    return os.path.join(*paths)


def convert_class_name_to_module_name(class_name: str) -> str:
    module_name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()
    return module_name


def convert_module_name_to_class_name(module_name: str) -> str:
    class_name = module_name.title().replace('_', '')
    return class_name


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


def is_extension(directory_path: str) -> bool:
    return os.path.exists(directory_path)


def get_extension_values(workflows_old, workflows_new):
    extension_values = {}

    # Add modified workflows
    for i in range(len(workflows_old)):
        num_nodes_1 = len(workflows_old[i]["nodes"])
        num_nodes_2 = len(workflows_new[i]["nodes"])

        if num_nodes_1 < num_nodes_2:
            extension_values[workflows_old[i]
                             ["name"]] = num_nodes_1

    # Add new workflows
    for i in range(len(workflows_old), len(workflows_new)):
        extension_values[workflows_new[i]['name']] = 1

    return extension_values
