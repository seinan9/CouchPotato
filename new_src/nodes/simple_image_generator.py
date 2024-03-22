from node import Node
from helpers.storage_helper import StorageHelper
from helpers.resource_loader import ResourceLoader

class SimpleImageGenerator(Node):

    def __init__(self, output_dir: str, targets: dict, seed: int, cuda_id: int, num_images: int, model_id: str, steps: int, cfg: float) -> None:
        super().__init__("", output_dir)
        self.targets = targets
        self.seed = seed
        self.num_images = num_images
        self.steps = steps
        self.cfg = cfg
        self.model = ResourceLoader.load_text_to_image_model(model_id, cuda_id)

    def run(self) -> None:
        super().run()
        for compound in self.targets.keys():
            StorageHelper.create_dir(f'{self.output_dir}/{compound}')
            for target in [compound] + self.targets[compound]:
                for i in range(self.num_images):
                    image = self.model.generate_image(self.seed + i, target, self.steps, self.cfg)
                    StorageHelper.save_image(image, f'{self.output_dir}/{compound}/{target}_{i}.png')
