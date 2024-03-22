from node import Node
from helpers.storage_helper import StorageHelper
from helpers.resource_loader import ResourceLoader

class ImageFeatureExtractor(Node):

    def __init__(self, input_dir: str, output_dir: str, targets: dict, cuda_id: int, model_id: str) -> None:
        super().__init__(input_dir, output_dir)
        self.targets = targets
        self.model = ResourceLoader.load_image_to_vector_model(model_id, cuda_id)

    def run(self) -> None:
        super().run()
        for compound in self.targets.keys():
            StorageHelper.create_dir(f'{self.output_dir}/{compound}')
            file_names = StorageHelper.list_files(f'{self.input_dir}/{compound}')
            for file_name in file_names:
                image = StorageHelper.load_image(f'{self.input_dir}/{compound}/{file_name}.png')
                vector = self.model.extract_vector(image)
                StorageHelper.save_vector(vector, f'{self.output_dir}/{compound}/{file_name}.pt')

