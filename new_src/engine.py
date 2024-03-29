import importlib
import logging
import time

from utils import Utils


class Engine():

    def __init__(self, workflow_config: dict) -> None:
        self.logger = logging.getLogger(__name__)

        self.output_dir = workflow_config['output_dir']
        config_file_path = Utils.join_paths(
            self.output_dir, 'workflow_config.yaml')
        self.logger.info(f'Initializing run with output directory: {self.output_dir}')

        self.is_extension = Utils.is_extension(self.output_dir)
        self.extension_values = {}
        if not self.is_extension:
            Utils.create_dir(self.output_dir)
        else:
            self.logger.info(f'Identified extension to previous run')
            previous_workflow_config = Utils.load_config(config_file_path)
            self.is_extension = True
            self.extension_values = Utils.get_extension_values(
                previous_workflow_config['workflows'], workflow_config['workflows'])

        Utils.save_config(workflow_config, config_file_path)
        self.global_parameters = workflow_config.get('global_parameters', {})
        self.workflows = workflow_config['workflows']

    def start(self) -> None:
        self.logger.info('Starting the workflow engine')
        engine_start_time = time.time()

        # Iterate over each workflow
        for workflow in self.workflows:
            workflow_name = workflow['name']

            if self.is_extension and workflow_name not in self.extension_values.keys():
                self.logger.info(
                    f'Skipping workflow: {workflow_name} (extension)')
                continue

            self.logger.info(
                f'Executing workflow: {workflow_name}')
            workflow_start_time = time.time()

            # Create directory for the current workflow
            workflow_dir = Utils.join_paths(self.output_dir, workflow_name)
            if not self.is_extension:
                Utils.create_dir(workflow_dir)

            # Reset previous_node_dir
            previous_node_dir = None

            # Iterate over each node in the workflow
            node_counter = 0
            for node in workflow['nodes']:
                node_name = node['name']
                module_name = Utils.convert_to_module_name(node_name)
                node_dir = Utils.join_paths(
                    workflow_dir, f'{node_counter}_{module_name}')

                # Import the node class dynamically
                module = importlib.import_module(f'nodes.{module_name}')
                node_class = getattr(module, node_name)

                # Combine global and specified node parameters
                specified_parameters = node.get('parameters', {})
                available_parameters = Utils.combine_parameters(
                    self.global_parameters, specified_parameters)

                # Get required parameters
                required_parameters = node_class.PARAMETERS

                # Assign default values for input_dir and output_dir if not provided
                default_parameters = [
                    ('input_dir', previous_node_dir),
                    ('output_dir', node_dir)
                ]
                for param_name, default_value in default_parameters:
                    if param_name in required_parameters and param_name not in available_parameters:
                        available_parameters[param_name] = default_value

                # Check for missing required parameters
                missing_parameters = [
                    param for param in required_parameters if param not in available_parameters]
                if missing_parameters:
                    error_msg = f'Missing required parameters for node {module_name} in workflow {workflow_name}: {", ".join(missing_parameters)}'
                    self.logger.error(error_msg)
                    raise ValueError(error_msg)

                # Prepare parameters for node instantiation
                parameters = {key: available_parameters[key]
                              for key in required_parameters.keys()}

                # Check if node has to be skipped
                if self.is_extension and node_counter < self.extension_values[workflow_name]:
                    self.logger.info(
                        f'Skipping node: {module_name} in workflow: {workflow_name} (extension)')
                    node_counter += 1
                    previous_node_dir = parameters["output_dir"]
                    continue

                # Instantiate and run the node
                self.logger.info(
                    f'Executing node: {module_name} in workflow: {workflow_name}')
                node_start_time = time.time()
                node_instance = node_class(**parameters)
                node_instance.run()

                # Update the previous node counter and directory
                node_counter += 1
                previous_node_dir = node_dir

                # Calculate node execution time
                node_execution_time = round(time.time() - node_start_time, 2)
                self.logger.info(
                    f'Node execution completed: {module_name} in workflow: {workflow_name} (Execution time: {node_execution_time:.2f}s)')

            # Calculate workflow execution time
            workflow_execution_time = round(
                time.time() - workflow_start_time, 2)
            self.logger.info(
                f'Workflow execution completed: {workflow_name} (Execution time: {workflow_execution_time:.2f}s)')

        # Calculate total execution time
        total_execution_time = round(time.time() - engine_start_time, 2)
        self.logger.info(
            f'All workflows executed successfully (Total execution time: {total_execution_time:.2f}s)')
