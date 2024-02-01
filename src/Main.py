from SDXLTurbo import SDXLTurbo
from DatasetGenerator import DatasetGenerator

image_generator = SDXLTurbo()
dg = DatasetGenerator(".data", "pancake_dataset", "pancake", ["pan", "cake"])
dg.generate_simple_dataset(image_generator, None, 3, 1, 1)
