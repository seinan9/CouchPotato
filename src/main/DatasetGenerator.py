import os
from ImageGenerator import ImageGenerator

class DatasetGenerator:

    def __init__(self, image_generator: ImageGenerator, data_dir: str, compound: str, components: list[str]):
        self.__image_generator = image_generator
        self.__data_dir = data_dir
        self.__compound = compound
        self.__components = components
    
    def generate_simple_dataset(self, n_train: int, n_test: int, n_validation: int, num_inference_steps: int = 50):
        self.create_directory_structure()
        self.generate_data_for_word(self.__comound, n_train, n_test, n_validation)
        for component in self.__components:
            self.generate_data_for_word(component, n_train, n_test, n_validation)

    def generate_data_for_word(self, word, n_train, n_test, n_validation, num_inference_steps: int = 50):
        word = [f"a {word}"] * (n_train + n_test + n_validation)
        images = self.__image_generator.generate_images(word)
        for i in range(n_train):
            images[i].save(f"{self.__data_dir}/datasets/{self.__compound}_datasets/train/{word}/{i}_{word}")
        for i in range(n_train, n_test):
            images[i].save(f"{self.__data_dir}/datasets/{self.__compound}_datasets/test/{word}/{i}_{word}")
        for i in range(n_train, n_validation):
            images[i].save(f"{self.__data_dir}/datasets/{self.__compound}_datasets/validation/{word}/{i}_{word}")
    
    def create_directory_structure(self):
        os.makedirs(f"{self.__data_dir}/datasets/{self.__compound}_dataset/train")
        os.makedirs(f"{self.__data_dir}/datasets/{self.__compound}_dataset/test")
        os.makedirs(f"{self.__data_dir}/datasets/{self.__compound}_dataset/validation")

        for i in range(self.components):
            os.makedirs(f"{self.__data_dir}/datasets/{self.__compound}_dataset/train/{self.__components[i]}")
            os.makedirs(f"{self.__data_dir}/datasets/{self.__compound}_dataset/test/{self.components[i]}")
            os.makedirs(f"{self.__data_dir}/datasets/{self.__compound}_dataset/validation/{self.__components[i]}")

if __name__ == "__main__":
    dg = DatasetGenerator(None, None, "jellyfish", ["jelly", "fish"])
    dg.generate_simple_dataset(10, 3, 3, 5)
