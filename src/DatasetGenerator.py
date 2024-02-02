import os
from image_generators.ImageGenerator import ImageGenerator


# Class that handles the generation of datasets.
class DatasetGenerator:

    @staticmethod
    def generate_simple_dataset(output_dir: str, compound: str, constituents: list[str], n_images: int, image_generator: ImageGenerator) -> None:
        os.makedirs(f'{output_dir}')

        for word in [compound] + constituents:
            images = image_generator.generate_image([word] * n_images)

            for i, image in enumerate(images):
                image.save(f'{output_dir}/{word}_{i}.png')

