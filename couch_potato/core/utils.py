import logging
import re

import yaml


def setup_logging(log_file: str) -> None:
    """
    Configure logging to output both to console and a file in the output directory.

    Args:
        output_dir (Path): Directory where log file will be saved.
    """
    log_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    # File handler
    file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
    file_handler.setFormatter(log_formatter)

    # Root logger config
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)


def load_yaml(file_path: str) -> dict:
    """
    Load a YAML file from the given path and return its contents as a dictionary.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data


def save_yaml(data: dict, file_path: str) -> None:
    """
    Save a dictionary as a YAML file to the specified path.
    Uses block style and preserves key order.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)


def convert_class_name_to_module_name(class_name: str) -> str:
    """
    Convert a CamelCase class name to a snake_case module name.
    Example: "ImagePreprocessor" -> "image_preprocessor"
    """
    module_name = re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()
    return module_name


def convert_module_name_to_class_name(module_name: str) -> str:
    """
    Convert a snake_case module name to a CamelCase class name.
    Example: "image_preprocessor" -> "ImagePreprocessor"
    """
    class_name = module_name.title().replace("_", "")
    return class_name


def combine_parameters(global_parameters: dict, node_parameters: dict) -> dict:
    """
    Merge two dictionaries, giving precedence to node_parameters.
    Parameters from global_parameters are added only if missing in node_parameters.
    """
    # If either dictionary is empty, return the other one
    if not global_parameters:
        return node_parameters if node_parameters else {}
    if not node_parameters:
        return global_parameters if global_parameters else {}

    # Combine dictionaries, preferring node_parameters
    combined_parameters = node_parameters.copy()
    for parameter, value in global_parameters.items():
        if parameter not in combined_parameters:
            combined_parameters[parameter] = value
    return combined_parameters


def resolve_placeholders(params: dict, current_index: int, node_dirs: dict) -> dict:
    """
    Recursively resolve placeholder strings in parameters.

    Supported placeholders:
    - ${this}       : Path to the current node directory
    - ${prev}       : Path to the previous node directory
    - ${node:<idx>} : Path to the <idx>-th node directory

    Args:
        params (dict): Dictionary of parameters
        current_index (int): Index of the current node (1-based)
        node_dirs (dict[int, Path]): Mapping from node index to its Path

    Returns:
        dict: Parameters with placeholders resolved
    """

    def _resolve(value):
        if isinstance(value, str):
            # ${this}
            if "${this}" in value:
                value = value.replace("${this}", str(node_dirs.get(current_index, "")))
            # ${prev}
            if "${prev}" in value:
                value = value.replace(
                    "${prev}", str(node_dirs.get(current_index - 1, ""))
                )

            # ${node:<idx>}
            def replace_node(match):
                node_idx = int(match.group(1))
                if node_idx not in node_dirs:
                    raise ValueError(
                        f"Placeholder references undefined node index: {node_idx}"
                    )
                return str(node_dirs[node_idx])

            value = re.sub(r"\$\{node:(\d+)\}", replace_node, value)
        elif isinstance(value, dict):
            value = {k: _resolve(v) for k, v in value.items()}
        elif isinstance(value, list):
            value = [_resolve(v) for v in value]
        return value

    return {k: _resolve(v) for k, v in params.items()}
