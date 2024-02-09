from PIL import Image
from torch import nn
from torch import Tensor
from torchvision import transforms
from torchvision.models import vit_h_14
from torchvision.models import ViT_H_14_Weights

from models.img2vec_model import Img2VecModel


class ViT(Img2VecModel):

    def __init__(self, cuda_id: int) -> None:
        self.cuda_id = cuda_id
        self.model = vit_h_14(weights=ViT_H_14_Weights.DEFAULT)
        self.model.heads = nn.Sequential(*list(self.model.heads.children())[:-1])
        self.model.to(self.cuda_id)


    def create_vector(self, image: Image) -> Tensor:
        transformations = transforms.Compose([transforms.ToTensor(),
                                transforms.Normalize(
                                    (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
                                transforms.Resize((518, 518))])
        image = transformations(image).float().unsqueeze_(0).to(self.cuda_id)
        return self.model(image).squeeze(0).detach().cpu()
