import importlib
import logging
import time

from core.utils import (combine_parameters,
                        convert_module_name_to_class_name,
                        create_dir,
                        get_extension_values,
                        is_extension,
                        join_paths,
                        load_config,
                        save_config)


class Engine():

    def __init__(self, config: dict) -> None:
        self.logger = logging.getLogger(__name__)
        self.root_output_dir = config['root_output_dir']
        config_file_path = join_paths(
            self.root_output_dir, 'config.yaml')
        self.logger.info(
            f'Initializing run with root output directory: {self.root_output_dir}')

        # Check if the run is an extension
        self.is_extension = is_extension(self.root_output_dir)
        self.extension_values = {}
        if not self.is_extension:
            create_dir(self.root_output_dir)
        else:
            self.logger.info(f'Identified extension to previous run')
            previous_workflow_config = load_config(config_file_path)
            self.is_extension = True
            self.extension_values = get_extension_values(
                previous_workflow_config['workflows'], config['workflows'])

        save_config(config, config_file_path)

         # Set global parameters and workflows
        self.global_parameters = config.get('global_parameters', {})
        self.workflows = config['workflows']

    def start(self) -> None:
        self.logger.info('Starting the workflow engine')
        engine_start_time = time.time()

        for workflow in self.workflows:
            workflow_name = workflow['name']

            if self.is_extension and workflow_name not in self.extension_values.keys():
                self.logger.info(
                    f'Skipping workflow: {workflow_name} (extension)')
                continue

            self.logger.info(
                f'Executing workflow: {workflow_name}')
            workflow_start_time = time.time()

            workflow_dir = join_paths(self.root_output_dir, workflow_name)
            if not self.is_extension:
                create_dir(workflow_dir)

            node_counter = 1
            previous_node_dir = None

            for node in workflow['nodes']:
                node_name = node['name']
                node_dir = join_paths(
                    workflow_dir, f'{node_counter}_{node_name}')
                class_name = convert_module_name_to_class_name(node_name)

                # Import the node class dynamically
                module = importlib.import_module(f'task.nodes.{node_name}')
                node_class = getattr(module, class_name)

                # Combine global and specified node parameters
                specified_parameters = node.get('parameters', {})
                available_parameters = combine_parameters(
                    self.global_parameters, specified_parameters)

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
                    error_msg = f'Missing required parameters for node {node_name} in workflow {workflow_name}: {", ".join(missing_parameters)}'
                    self.logger.error(error_msg)
                    raise ValueError(error_msg)

                # Prepare parameters for node instantiation
                parameters = {key: available_parameters[key]
                              for key in required_parameters.keys()}

                # Skip node if was already executed in a previous run
                if self.is_extension and node_counter < self.extension_values[workflow_name]:
                    self.logger.info(
                        f'Skipping node: {node_name} in workflow: {workflow_name} (extension)')
                    node_counter += 1
                    previous_node_dir = parameters["output_dir"]
                    continue

                # Instantiate and run the node
                self.logger.info(
                    f'Executing node: {node_name} in workflow: {workflow_name}')
                node_start_time = time.time()
                node_instance = node_class(**parameters)
                node_instance.run()

                node_counter += 1
                previous_node_dir = node_dir

                node_execution_time = round(time.time() - node_start_time, 2)
                self.logger.info(
                    f'Node execution completed: {node_name} in workflow: {workflow_name} (Execution time: {node_execution_time:.2f}s)')

            workflow_execution_time = round(
                time.time() - workflow_start_time, 2)
            self.logger.info(
                f'Workflow execution completed: {workflow_name} (Execution time: {workflow_execution_time:.2f}s)')

        total_execution_time = round(time.time() - engine_start_time, 2)
        self.logger.info(
            f'All workflows executed successfully (Total execution time: {total_execution_time:.2f}s)')
