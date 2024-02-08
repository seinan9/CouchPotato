import torchvision
from PIL import Image
from torch import nn
from torchvision import transforms as tr
from torchvision.models import vit_h_14
import torch
import numpy as np

from models.img2vec_model import Img2VecModel

# TODO: Update
class ViT(Img2VecModel):

    def __init__(self):
        weights = torchvision.models.ViT_H_14_Weights.DEFAULT
        self.model = vit_h_14(weights=weights)
        self.model.heads = nn.Sequential(
            *list(self.model.heads.children())[:-1])
        self.model = self.model.to("cuda:0")

    def generate_embedding(self, img):
        transformations = tr.Compose([tr.ToTensor(),
                                tr.Normalize(
                                    (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
                                tr.Resize((518, 518))])
        img = transformations(img).float().unsqueeze_(0).to('cuda:0')
        return self.model(img).detach().cpu()
