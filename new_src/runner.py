import importlib

from helpers.storage_helper import StorageHelper
from helpers.utils import Utils

# Executes the workflows
class Runner():

    def __init__(self, workflow_config):
        self.output_dir = workflow_config['output_dir']
        self.global_parameters = workflow_config.get('global_parameters', {})
        self.workflows = workflow_config['workflows']
        StorageHelper.create_dir(self.output_dir)
        StorageHelper.save_yaml(workflow_config, f'{self.output_dir}/workflow_config.yaml')

    def run(self):
        for workflow in self.workflows:
            workflow_name = workflow['name']
            workflow_dir = f'{self.output_dir}/{workflow_name}'
            StorageHelper.create_dir(workflow_dir)
            previous_node_dir = None

            for node in workflow['nodes']:
                node_name = node['name']
                node_dir = f'{workflow_dir}/{node_name}'
                StorageHelper.create_dir(node_dir)

                module_name = Utils.convert_to_module_name(node_name)
                module = importlib.import_module(f'nodes.{module_name}')
                clazz = getattr(module, node_name)

                required_parameters = getattr(clazz, '__init__').__annotations__
                del required_parameters['return']
                node_parameters = node['parameters']
                available_parameters = Utils.combine_parameters(self.global_parameters, node_parameters)
                available_parameters['input_dir'] = previous_node_dir
                available_parameters['output_dir'] = node_dir
                parameters = [available_parameters[key] for key in required_parameters.keys()]

                node_instance = clazz(*parameters)
                node_instance.run()

                previous_node_dir = node_dir
