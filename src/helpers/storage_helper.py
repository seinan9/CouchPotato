import os
import json
from PIL import Image


class StorageHelper():

    # static variable that is set when create_data_dir() is called
    output_dir = None

    @staticmethod
    def set_output_dir(output_dir):
        StorageHelper.output_dir = output_dir

    @staticmethod
    def create_data_dir():
        os.makedirs(f'{StorageHelper.output_dir}/images')
        os.makedirs(f'{StorageHelper.output_dir}/vectors')
        os.makedirs(f'{StorageHelper.output_dir}/distances')

    @staticmethod
    def load_params(file):
        with open(file) as f:
            return json.load(f)

    @staticmethod
    def save_params(params):
        with open(f'{StorageHelper.output_dir}/params.json', 'w', encoding='utf-8') as f:
            json.dump(params, f, indent=4)

    @staticmethod
    def load_image(file_name):
        return Image.open(f'{StorageHelper.output_dir}/images/{file_name}.png')

    @staticmethod
    def save_image(image: Image, file_name):
        image.save(f'{StorageHelper.output_dir}/images/{file_name}.png')

    # TODO
    @staticmethod
    def save_vec(vec, file_name):
        pass

    # TODO
    @staticmethod
    def load_vec(file_name):
        pass

    @staticmethod
    def list_images():
        return os.listdir(f'{StorageHelper.output_dir}/images')