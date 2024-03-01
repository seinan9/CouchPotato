import csv
import json
import os
import logging

import torch
from natsort import natsorted
from PIL import Image

class StorageHelper():

    logger = logging.getLogger(__name__)

    # static variables that are set by the runner
    output_directory: str = ''
    words: list[str] = []

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
        StorageHelper.logger.info('Created output directory')

    @staticmethod
    def load_parameters(file: str) -> dict:
        with open(file) as f:
            parameters = json.load(f)

        StorageHelper.logger.info('Loaded parameters')
        return parameters

    @staticmethod
    def save_parameters(parameters: dict) -> None:
        with open(f'{StorageHelper.output_directory}/parameters.json', 'w', encoding='utf-8') as f:
            json.dump(parameters, f, indent=4)
        
        StorageHelper.logger.info('Saved parameters in output directory')

    @staticmethod
    def load_image(file_name: str) -> Image.Image:
        return Image.open(f'{StorageHelper.output_directory}/images/{file_name}.png')

    @staticmethod
    def save_image(image: Image.Image, file_name: str) -> None:
        image.save(f'{StorageHelper.output_directory}/images/{file_name}.png')

    @staticmethod
    def save_vector(vector: torch.Tensor, file_name: str) -> None:
        torch.save(
            vector, f'{StorageHelper.output_directory}/vectors/{file_name}.pt')

    @staticmethod
    def load_vector(file_name: str) -> torch.Tensor:
        return torch.load(f'{StorageHelper.output_directory}/vectors/{file_name}.pt')

    @staticmethod
    def load_all_vectors() -> dict[str, torch.Tensor]:
        file_names_separated = {f'{word}': [] for word in StorageHelper.words}
        file_names = StorageHelper.list_output_files('vectors')

        for file_name in file_names:
            for word in file_names_separated.keys():

                # This works solely because the file_names corresponding to the compound are processed first, since words[0] corresponds to the compound.
                # TODO: Find a more robust way, that is not dependent on the ordering of words[]
                if word in file_name:
                    file_names_separated[word].append(file_name)
                    break

        return {f'{word}': torch.stack([StorageHelper.load_vector(file_name) for file_name in file_names_separated[word]]) for word in StorageHelper.words}

    @staticmethod
    def save_distances(distances, file_name):
        with open(f'{StorageHelper.output_directory}/distances/{file_name}.tsv', 'w', newline='') as f:
            csvwriter = csv.DictWriter(f, fieldnames=distances.keys())
            csvwriter.writeheader()
            csvwriter.writerow(distances)

    @staticmethod
    def list_output_files(sub_directory: str) -> list[str]:
        return natsorted([file_name.split('.')[0] for file_name in os.listdir(f'{StorageHelper.output_directory}/{sub_directory}')])
