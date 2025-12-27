from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import os

class BlipCaptioner:
    def __init__(self):
        self.processor = BlipProcessor.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        self.model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )
        
    def generateCaption(self, imagePath: str) -> str:
        assert os.path.exists(imagePath), "Path to iamge doesn't exist"
        image = Image.open(imagePath).convert("RGB")
        inputs = self.processor(images = image, return_tensors = "pt")
        out = self.model.generate(**inputs) # type: ignore
        
        return self.processor.decode(out[0], skip_special_tokens = True)