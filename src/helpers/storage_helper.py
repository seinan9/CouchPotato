import json
import os

import torch
from natsort import natsorted
from PIL.Image import Image
from PIL import Image as image


class StorageHelper():

    # static variables that are set by the runner
    output_directory: str = None
    words: list[str] = None

    @staticmethod
    def set_output_directory(output_directory: str) -> None:
        StorageHelper.output_directory = output_directory

    @staticmethod
    def set_words(words: list[str]) -> None:
        StorageHelper.words = words

    @staticmethod
    def create_output_directory() -> None:
        os.makedirs(f'{StorageHelper.output_directory}/images')
        os.makedirs(f'{StorageHelper.output_directory}/vectors')
        os.makedirs(f'{StorageHelper.output_directory}/distances')

    @staticmethod
    def load_parameters(file: str) -> dict:
        with open(file) as f:
            return json.load(f)

    @staticmethod
    def save_parameters(parameters: dict) -> None:
        with open(f'{StorageHelper.output_directory}/parameters.json', 'w', encoding='utf-8') as f:
            json.dump(parameters, f, indent=4)

    @staticmethod
    def load_image(file_name: str) -> Image:
        return image.open(f'{StorageHelper.output_directory}/images/{file_name}.png')

    @staticmethod
    def save_image(image: Image, file_name: str) -> None:
        image.save(f'{StorageHelper.output_directory}/images/{file_name}.png')

    @staticmethod
    def save_vector(vector: torch.Tensor, file_name: str) -> None:
        torch.save(
            vector, f'{StorageHelper.output_directory}/vectors/{file_name}.pt')

    @staticmethod
    def load_vector(file_name: str) -> torch.Tensor:
        return torch.load(f'{StorageHelper.output_directory}/vectors/{file_name}.pt')

    @staticmethod
    def list_output_files(sub_directory: str) -> list[str]:
        return natsorted([file_name.split('.')[0] for file_name in os.listdir(f'{StorageHelper.output_directory}/{sub_directory}')])
