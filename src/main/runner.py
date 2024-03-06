import argparse
import logging

from helpers.storage_helper import StorageHelper
from helpers.validator import Validator
from img2vec import Img2Vec
from txt2img import Txt2Img
from vec2dist import Vec2Dist
from txt2vec import Txt2Vec
from vec2vec import Vec2Vec


class Runner():

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--file', default='./parameters.json',
                            help='A json file containing the run parameters.')

        try:
            args = parser.parse_args()
        except argparse.ArgumentError as e:
            self.logger.error(e)

        self.parameters = StorageHelper.load_parameters(args.file)
        if not Validator.validate(self.parameters):
            self.logger.error('Shutdown due to faulty parameters')
            exit()

        StorageHelper.set_output_directory(
            self.parameters['general']['output_dir'])
        StorageHelper.set_words(self.parameters['general']['words'])
        StorageHelper.create_output_directory()
        StorageHelper.save_parameters(self.parameters)

    def run(self) -> None:
        if self.parameters['visual']['run']:
            StorageHelper.set_approach('visual')
            getattr(Txt2Img, self.parameters['visual']['txt2img_method'])(
                *self.parameters['visual']['txt2img_parameters'])
            getattr(Img2Vec, self.parameters['visual']['img2vec_method'])(
                *self.parameters['visual']['img2vec_parameters'])
            getattr(Vec2Dist, self.parameters['visual']['vec2dist_method'])(
                *self.parameters['visual']['vec2dist_parameters'])
        
        if self.parameters['textual']['run']:
            StorageHelper.set_approach('textual')
            getattr(Txt2Vec, self.parameters['textual']['txt2vec_method'])(*self.parameters['textual']['txt2vec_parameters'])
            getattr(Vec2Dist, self.parameters['textual']['vec2dist_method'])(*self.parameters['textual']['vec2dist_parameters'])

        if self.parameters['combined']['run']:
            StorageHelper.set_approach('combined')
            getattr(Vec2Vec, self.parameters['combined']['vec2vec_method'])(*self.parameters['combined']['vec2vec_parameters'])
            getattr(Vec2Dist, self.parameters['combined']['vec2dist_method'])(*self.parameters['combined']['vec2dist_parameters'])


if __name__ == "__main__":
    runner = Runner()
    runner.run()
