import torch
import torchvision

from PIL.Image import Image

from resources.image_to_vector_models.image_to_vector_model import ImageToVectorModel


class VisionTransformer(ImageToVectorModel):

    def __init__(self, cuda_id: int) -> None:
        self.cuda_id = cuda_id
        self.model = torchvision.models.vit_h_14(weights=torchvision.models.ViT_H_14_Weights.DEFAULT)
        self.model.heads = torch.nn.Sequential(*list(self.model.heads.children())[:-1])
        self.model.to(self.cuda_id)


    def extract_vector(self, image: Image) -> torch.Tensor:
        transformations = torchvision.transforms.Compose([torchvision.transforms.ToTensor(),
                                torchvision.transforms.Normalize(
                                    (0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
                                torchvision.transforms.Resize((518, 518))])
        image = transformations(image).float().unsqueeze_(0).to(self.cuda_id)
        return self.model(image).squeeze(0).detach().cpu()
