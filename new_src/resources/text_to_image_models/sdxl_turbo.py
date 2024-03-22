import torch

from diffusers.pipelines.auto_pipeline import AutoPipelineForText2Image
from PIL.Image import Image

from resources.text_to_image_models.text_to_image_model import TextToImageModel

class SdxlTurbo(TextToImageModel):

    def __init__(self, cuda_id: str) -> None:
        self.pipe = AutoPipelineForText2Image.from_pretrained(pretrained_model_or_path='stabilityai/sdxl-turbo', torch_dtype=torch.float16, variant='fp16').to(cuda_id)
    
    def generate_image(self, seed: int, prompt: str, steps: int, cfg: float) -> Image:
        generator = torch.manual_seed(seed)
        with torch.no_grad():
            return self.pipe(prompt=prompt, num_inference_steps=steps, classifier_guidance=cfg, generator=generator).images[0]
