import torch
import open_clip
from PIL import Image

class ClipEmbedder:
    def __init__(self):
        self.model, _, self.preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32", pretrained = "openai"
        )
        self.tokenizer = open_clip.get_tokenizer("ViT-B-32")
        
    def encodeImage(self, imagePath: str):
        image = Image.open(imagePath).convert("RGB")
        imageTensor = self.preprocess(image).unsqueeze(0) # type: ignore
        with torch.no_grad():
            emb = self.model.encode_image(imageTensor) # type: ignore
            
        return emb[0].cpu().numpy().tolist()
    
    def encodeText(self, text: str):
        tokens = self.tokenizer([text])
        with torch.no_grad():
            emb = self.model.encode_text(tokens) # type: ignore
        return emb[0].cpu().numpy().tolist()