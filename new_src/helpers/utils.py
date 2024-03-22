import re

class Utils():

    @staticmethod
    def convert_to_module_name(class_name: str) -> str:
        module_name = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()
        return module_name
    
    @staticmethod
    def combine_parameters(global_parameters: dict, node_parameters: dict) -> dict:
        combined_parameters = node_parameters
        for parameter in global_parameters.keys():
            if parameter not in node_parameters.keys():
                combined_parameters[parameter] = global_parameters[parameter]
        return combined_parameters
