import importlib
import logging
import shutil
import time
from pathlib import Path

from couch_potato.core.utils import (
    combine_parameters,
    convert_module_name_to_class_name,
)


class Engine:
    """
    Engine for executing a single workflow defined as a dictionary.

    The workflow contains:
    - output_dir: directory path for all outputs and artifacts
    - global_parameters: parameters shared by all nodes
    - nodes: list of nodes, each specifying a task to execute with parameters

    The Engine manages:
    - Creating output directories
    - Saving the workflow config for reproducibility
    - Dynamically loading node classes
    - Combining global and node-specific parameters
    - Running each node sequentially and logging execution times
    """

    def __init__(self, workflow: dict, output_dir: Path) -> None:
        """
        Initialize the Engine with the workflow configuration and output directory.

        Args:
            workflow (dict): Parsed workflow configuration.
                - global_parameters (dict, optional): Shared parameters for all nodes.
                - nodes (list): Node configurations with 'name' and optional 'parameters'.
            output_dir (Path): Directory to store artifacts and logs.
        """

        logging.info("Preparing workflow execution")
        self.global_parameters = workflow.get("global_parameters", {})
        self.nodes = workflow.get("nodes", [])
        self.output_dir = output_dir

        logging.info("Output directory: %s", output_dir)
        logging.info("Nodes: %d", len(self.nodes))

    def start(self) -> None:
        """
        Execute all nodes in the workflow sequentially.

        For each node:
        - Dynamically import the node class
        - Combine global and node parameters (node-specific override)
        - Set default input/output directories if missing
        - Check required parameters are present
        - Instantiate and run the node
        - Log execution time

        Also logs total workflow execution time.
        """
        logging.info("Executing workflow")
        workflow_start_time = time.time()

        artifacts_dir = self.output_dir / "artifacts"
        artifacts_dir.mkdir(exist_ok=True)

        previous_node_dir = None
        resume_from_here = False

        for index, node in enumerate(self.nodes, start=1):
            node_name = node["name"]
            class_name = convert_module_name_to_class_name(node_name)

            # Directory to store all node-specific outputs/artifacts
            node_dir = artifacts_dir / f"{index}_{node_name}"
            flag_file = node_dir / "in_progress.flag"

            # If resuming from an invalidated node, clear all following
            if resume_from_here:
                if node_dir.exists():
                    logging.info(
                        "[%d/%d] Invalidating node: %s. Downstream of failed node. Clearing artifacts.",
                        index,
                        len(self.nodes),
                        node_name,
                    )
                    shutil.rmtree(node_dir, ignore_errors=True)

            # Handle rerun logic for current node
            if flag_file.exists():
                logging.info(
                    "[%d/%d] Detected incomplete execution for node: %s. Clearing directory for rerun",
                    index,
                    len(self.nodes),
                    node_name,
                )
                shutil.rmtree(node_dir, ignore_errors=True)
                node_dir.mkdir(parents=True, exist_ok=True)
                resume_from_here = True  # Invalidate downstream nodes

            elif node_dir.exists():
                logging.info(
                    "[%d/%d] Skipping node: %s. Previously executed successfully (marker file missing, assuming valid artifacts)",
                    index,
                    len(self.nodes),
                    node_name,
                )
                previous_node_dir = node_dir
                continue

            # Dynamically import the node's class from the task.nodes package
            module = importlib.import_module(f"task.nodes.{node_name}")
            node_class = getattr(module, class_name)

            # Combine global and node parameters, with node parameters taking precedence
            specified_parameters = node.get("parameters", {})
            available_parameters = combine_parameters(
                self.global_parameters, specified_parameters
            )

            # Get the set of parameters the node class requires
            required_parameters = node_class.PARAMETERS

            # Assign default input_dir and output_dir if missing but required
            default_parameters = [
                ("input_dir", previous_node_dir),
                ("output_dir", node_dir),
            ]
            for param_name, default_value in default_parameters:
                if (
                    param_name in required_parameters
                    and param_name not in available_parameters
                ):
                    available_parameters[param_name] = default_value

            # Validate all required parameters are provided
            missing_parameters = [
                param
                for param in required_parameters
                if param not in available_parameters
            ]
            if missing_parameters:
                error_msg = f'Missing required parameters for node {node_name}: {", ".join(missing_parameters)}'
                logging.error(error_msg)
                raise ValueError(error_msg)

            # Filter parameters to only those required by the node class
            parameters = {
                key: available_parameters[key] for key in required_parameters.keys()
            }

            # Create node directory and flag
            node_dir.mkdir(exist_ok=True)
            flag_file.touch()

            # Instantiate and run the node
            logging.info(
                "[%d/%d] Executing node: %s", index, len(self.nodes), node_name
            )

            node_start_time = time.time()
            node_instance = node_class(**parameters)
            node_instance.run()

            # Mark as complete
            flag_file.unlink()

            previous_node_dir = node_dir

            node_execution_time = time.time() - node_start_time
            logging.info(
                "[%d/%d] Executed node: %s in %.2fs",
                index,
                len(self.nodes),
                node_name,
                node_execution_time,
            )

        workflow_execution_time = time.time() - workflow_start_time
        logging.info(
            "Executed workflow in %.2fs",
            workflow_execution_time,
        )
