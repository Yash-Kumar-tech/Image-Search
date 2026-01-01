import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import os
import gc

class FlorenceCaptioner:
    _instance = None
    _model = None
    _processor = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FlorenceCaptioner, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if FlorenceCaptioner._model is None:
            self.modelId = "microsoft/Florence-2-base"
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"FlorenceCaptioner: Using device: {self.device}")
            
            self.torchDtype = torch.float16 if self.device == "cuda" else torch.float32
            
            FlorenceCaptioner._model = AutoModelForCausalLM.from_pretrained(
                self.modelId, 
                trust_remote_code=True,
                torch_dtype=self.torchDtype
            ).to(self.device)
            
            FlorenceCaptioner._processor = AutoProcessor.from_pretrained(
                self.modelId, 
                trust_remote_code=True
            )
        
        self.model = FlorenceCaptioner._model
        self.processor = FlorenceCaptioner._processor

    def _preprocessImage(self, imagePath: str, maxDim: int = 768) -> Image.Image:
        img = Image.open(imagePath).convert("RGB")
        if max(img.size) > maxDim:
            img.thumbnail((maxDim, maxDim), Image.Resampling.LANCZOS)
        return img

    def generateCaption(self, imagePath: str) -> str:
        # Resize to save memory
        image = self._preprocessImage(imagePath, maxDim=768)
        prompt = "<DETAILED_CAPTION>"
        
        inputs = self.processor(text=prompt, images=image, return_tensors="pt").to(self.device, self.torchDtype)
        
        with torch.no_grad():
            generatedIds = self.model.generate(
                input_ids=inputs["input_ids"],
                pixel_values=inputs["pixel_values"],
                max_new_tokens=128,
                num_beams=3
            )
        
        generatedText = self.processor.batch_decode(generatedIds, skip_special_tokens=False)[0]
        parsedAnswer = self.processor.post_process_generation(generatedText, task=prompt, image_size=(image.width, image.height))
        
        # Cleanup
        del inputs
        del generatedIds
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        return parsedAnswer[prompt]

    def encodeImage(self, imagePath: str) -> list[float]:
        image = self._preprocessImage(imagePath, maxDim=768)
        inputs = self.processor(text="<DETAILED_CAPTION>", images=image, return_tensors="pt").to(self.device, self.torchDtype)
        
        with torch.no_grad():
            vision_outputs = self.model.vision_tower(inputs["pixel_values"])
            embeddings = vision_outputs.last_hidden_state.mean(dim=1).squeeze(0).to(torch.float32)
            
        # Cleanup
        del inputs
        del vision_outputs
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        return embeddings.cpu().numpy().tolist()

    def encodeText(self, text: str) -> list[float]:
        inputs = self.processor(text=text, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.model.encoder(input_ids=inputs["input_ids"], attention_mask=inputs.get("attention_mask"))
            embeddings = outputs.last_hidden_state.mean(dim=1).squeeze(0).to(torch.float32)
            
        return embeddings.cpu().numpy().tolist()
