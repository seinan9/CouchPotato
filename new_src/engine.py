import importlib
import logging
import time

from utils import Utils


class Engine():

    def __init__(self, workflow_config: dict) -> None:
        self.logger = logging.getLogger(__name__)
        self.output_dir = workflow_config['output_dir']
        self.global_parameters = workflow_config.get('global_parameters', {})
        self.workflows = workflow_config['workflows']
        Utils.create_dir(self.output_dir)
        Utils.save_config(
            workflow_config, f'{self.output_dir}/workflow_config.yaml')

    def run(self) -> None:
        total_time = time.time()
        self.logger.info('Starting workflow engine')
        for workflow in self.workflows:
            workflow_start_time = time.time()
            workflow_name = workflow['name']
            self.logger.info(
                f'Starting execution of workflow: {workflow_name}')
            workflow_dir = f'{self.output_dir}/{workflow_name}'
            Utils.create_dir(workflow_dir)
            previous_node_dir = None

            for node in workflow['nodes']:
                node_start_time = time.time()
                node_name = node['name']
                module_name = Utils.convert_to_module_name(node_name)
                self.logger.info(f'Starting execution of node: {module_name}')
                node_dir = f'{workflow_dir}/{module_name}'

                # Dynamically import the node class
                module = importlib.import_module(f'nodes.{module_name}')
                node_class = getattr(module, node_name)

                # Combine global and specified parameters
                specified_parameters = node.get('parameters', {})
                available_parameters = Utils.combine_parameters(
                    self.global_parameters, specified_parameters)

                # Get required parameters
                required_parameters = node_class.PARAMETERS

                # Assign default values for input_dir and output_dir if not provided
                if 'input_dir' in required_parameters.keys():
                    if 'input_dir' not in available_parameters.keys():
                        available_parameters['input_dir'] = previous_node_dir

                if 'output_dir' in required_parameters.keys():
                    if 'output_dir' not in available_parameters.keys():
                        available_parameters['output_dir'] = node_dir

                # Ensure required parameters are provided
                missing_parameters = [
                    param for param in required_parameters if param not in available_parameters]
                if missing_parameters:
                    error_msg = f'Missing required parameters for node {module_name}: {", ".join(missing_parameters)}'
                    self.logger.error(error_msg)
                    raise ValueError(error_msg)

                # Prepare parameters for node instantiation
                parameters = {key: available_parameters[key]
                              for key in required_parameters.keys()}

                # Instantiate and run the node
                node_instance = node_class(**parameters)
                node_instance.run()

                # Update the previous node directory
                previous_node_dir = node_dir

                node_execution_time = round(time.time() - node_start_time, 2)
                self.logger.info(
                    f'Finished execution of node: {module_name} ({node_execution_time:.2f}s)')

            workflow_execution_time = round(
                time.time() - workflow_start_time, 2)
            self.logger.info(
                f'Finished execution of workflow: {workflow_name} ({workflow_execution_time:.2f}s)')

        total_execution_time = round(time.time() - total_time, 2)
        self.logger.info(
            f'Finished executing all workflows ({total_execution_time:.2f}s)')
