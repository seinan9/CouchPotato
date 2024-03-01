import logging
import importlib
import inspect


class Validator():

    logger = logging.getLogger(__name__)

    @staticmethod
    def validate(parameters: dict) -> bool:
        if not Validator.validate_keys(parameters):
            return False
        if not Validator.validate_flow(parameters):
            return False
        if not Validator.validate_methods(parameters):
            return False
        
        Validator.logger.info('Validated parameters')
        return True

    @staticmethod
    def validate_keys(parameters: dict) -> bool:
        schema = {
            "general": ["output_dir", "words", "seed", "cuda_id"],
            "visual": ["run", "txt2img_method", "txt2img_parameters", "img2vec_method", "img2vec_parameters", "vec2dist_method", "vec2dist_parameters"],
            "textual": ["run", "txt2vec_method", "txt2vec_parameters", "vec2dist_method", "vec2dist_parameters"],
            "combined": ["run", "vec2vec_method", "vec2vec_parameters", "vec2dist_method", "vec2dist_parameters"]
        }

        if sorted(schema.keys()) != sorted(parameters.keys()):
            logging.error(f'ValidationError: wrong keys')
            return False
        
        for key in schema.keys():
            if sorted(schema[key]) != sorted(parameters[key].keys()):
                Validator.logger.error(
                    f'ValidationError: wrong keys')
                return False
            
        return True

    @staticmethod
    def validate_methods(parameters: dict) -> bool:
        methods = {
            "visual": ["Txt2Img", "Img2Vec", "Vec2Dist"],
            "textual": ["Txt2Vec", "Vec2Dist"],
            "combined": ["Vec2Vec", "Vec2Dist"]
        }

        for approach in methods.keys():
            if parameters[approach]['run'] == True:
                for method_name in methods[approach]:
                    module = importlib.import_module(method_name.lower())
                    clazz = getattr(module, method_name)

                    try:
                        method = getattr(clazz, parameters[approach][f'{method_name.lower()}_method'])
                    except:
                        Validator.logger.error(f'ValidationError: method not found')
                        return False
                    
                    arguments = parameters[approach][f'{method_name.lower()}_parameters']
                    if len(inspect.signature(method).parameters) != len(arguments):
                        Validator.logger.error(f'ValidationError: wrong method signature')
                        return False
                    
        return True

    @staticmethod
    def validate_flow(parameters: dict) -> bool:
        if parameters['combined']['run'] == True:
            if parameters['visual']['run'] == False or parameters['textual']['run'] == False:
                Validator.logger.error(
                    f'ValidationError: combined requires visual and textual')
                return False
            
        return True
