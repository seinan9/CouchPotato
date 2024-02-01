import os
from ImageGenerator import ImageGenerator

# Class that handles the generation of datasets.


class DatasetGenerator:

    data_dir = None
    dataset_id = None
    words = None

    def __init__(self, data_dir: str, dataset_id: str, compound: str, constituents: list[str]):
        self.data_dir = data_dir
        self.dataset_id = dataset_id
        self.words = [compound] + [constituent for constituent in constituents]
        self.__create_directory_structure()

    # Generate images and store them in a dataset appropriate structure.
    def generate_dataset(self, image_generator: ImageGenerator, inference_params: list, prompts_train: dict, prompts_test: dict, prompts_validation: dict):
        for word in self.words:

            # Generate images
            images = []
            for prompt in (prompts_train[word] + prompts_test[word] + prompts_validation[word]):
                images += image_generator.generate_image(prompt)

            # Store images
            n_train = len(prompts_train[word])
            n_test = len(prompts_test[word])
            n_validation = len(prompts_validation[word])
            for i in range(n_train):
                images[i].save(
                    f"{self.data_dir}/datasets/{self.dataset_id}/train/{word}/{i}_{word}.png")
            for i in range(n_train, n_train + n_test):
                images[i].save(
                    f"{self.data_dir}/datasets/{self.dataset_id}/test/{word}/{i}_{word}.png")
            for i in range(n_train + n_test, n_train + n_test + n_validation):
                images[i].save(
                    f"{self.data_dir}/datasets/{self.dataset_id}/validation/{word}/{i}_{word}.png")

    # Generate a simple dataset without specifying prompts.
    # The propmts are of the form "a word".
    def generate_simple_dataset(self, image_generator: ImageGenerator, inference_params: list, n_train: int, n_test: int, n_validation: int):
        prompts_train = {}
        prompts_test = {}
        prompts_validation = {}

        for word in self.words:
            prompts_train[word] = [word] * n_train
        for word in self.words:
            prompts_test[word] = [word] * n_test
        for word in self.words:
            prompts_validation[word] = [word] * n_validation

        self.generate_dataset(image_generator, inference_params,
                              prompts_train, prompts_test, prompts_validation)

    # Create directory structure where images are stored and loaded from.
    def __create_directory_structure(self):
        for split in ["train", "test", "validation"]:
            os.makedirs(f"{self.data_dir}/datasets/{self.dataset_id}/{split}")
            for word in self.words:
                os.makedirs(
                    f"{self.data_dir}/datasets/{self.dataset_id}/{split}/{word}")
        print(f"Created directories for dataset with id {self.dataset_id}.")
