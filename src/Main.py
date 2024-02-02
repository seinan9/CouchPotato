import json
from Loader import Loader
from DatasetGenerator import DatasetGenerator
from Similarity import Similarity

def load_params(params_dir):
    with open(params_dir) as json_file:
        params = json.load(json_file)
    return params

def execute_step_one(params):
    compound = params["0"]["compound"]
    constituents = params["0"]["constituents"]

    output_dir = params["1"]["output_dir"]
    n_images = params["1"]["n_images"]
    image_generator_id = params["1"]["image_generator_id"]
    image_generator_params = params["1"]["image_generator_params"]

    image_generator = Loader.get_image_generator(image_generator_id)
    DatasetGenerator.generate_simple_dataset(output_dir, compound, constituents, n_images, image_generator)

def execute_step_two(params):
    compound = params["0"]["compound"]
    constituents = params["0"]["constituents"]

    input_dir = params["2"]["input_dir"]
    output_dir = params["2"]["output_dir"]
    embedding_generator_id = params["2"]["embedding_generator_id"]
    embedding_generator_params = params["2"]["embedding_generator_params"]

    embedding_generator = Loader.get_embedding_generator(embedding_generator_id)
    embedding_generator.generate_embedding

if __name__ == "__main__":
    # params = load_params("params.json")
    # if params["1"]["active"] == "true":
    #     execute_step_one(params)

    eg = Loader.get_embedding_generator("ViT")
    emb0 = eg.generate_embedding(".data/cupcake/images/cupcake_0.png")
    emb1 = eg.generate_embedding(".data/cupcake/images/cake_0.png")
    sim = Similarity()
    cos = sim.get_cosine_similarity(emb0, emb1)
    print(type(cos[0]))
    print(cos)



# import embedding_generators.ViT
# img_path_1 = ".data/datasets/pancake_dataset/train/pancake/0_pancake.png"
# img_path_2 = ".data/datasets/pancake_dataset/train/cake/0_cake.png"
# img_path_3 = ".data/datasets/pancake_dataset/train/pan/0_pan.png"

# vit = embedding_generators.ViT.ViT()
# emb_1 = vit.generate_embedding(img_path_1)
# emb_2 = vit.generate_embedding(img_path_2)
# emb_3 = vit.generate_embedding(img_path_3)

# from Similarity import Similarity
# sim = Similarity()
# cos1 = sim.get_cosine_similarity(emb_1, emb_2)
# cos2 = sim.get_cosine_similarity(emb_1, emb_3)

# print(cos1, cos2)
