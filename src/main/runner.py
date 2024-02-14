import argparse

from helpers.storage_helper import StorageHelper
from img2vec import Img2Vec
from txt2img import Txt2Img
from vec2dist import Vec2Dist


class Runner():

    def __init__(self) -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--file', default='./parameters.json',
                            help='A json file containing the run parameters.')

        try:
            args = parser.parse_args()
        except argparse.ArgumentError as e:
            print(e)

        self.parameters = StorageHelper.load_parameters(args.file)
        StorageHelper.set_output_directory(self.parameters['output_dir'])
        StorageHelper.set_words(self.parameters['words'])
        StorageHelper.create_output_directory()
        StorageHelper.save_parameters(self.parameters)

    def run(self) -> None:
        getattr(Txt2Img, self.parameters['txt2img_method'])(
            *self.parameters['txt2img_params'])
        getattr(Img2Vec, self.parameters['img2vec_method'])(
            *self.parameters['img2vec_params'])
        getattr(Vec2Dist, self.parameters['vec2dist_method'])(
            *self.parameters['vec2dist_params'])


if __name__ == "__main__":
    runner = Runner()
    runner.run()
