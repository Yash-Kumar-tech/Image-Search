from transformers import AutoModelForImageTextToText, AutoProcessor, BitsAndBytesConfig
from transformers.utils import is_flash_attn_2_available
from qwen_vl_utils import process_vision_info
from PIL import Image
import os
import torch
import gc

class QwenCaptioner:
    _instance = None
    _model = None
    _processor = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QwenCaptioner, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Only initialize once
        if QwenCaptioner._model is None:
            self.modelId = "Qwen/Qwen3-VL-2B-Instruct"
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"QwenCaptioner: Using device: {self.device}")
            
            attnImplementation = "flash_attention_2" if is_flash_attn_2_available() else "sdpa"
            print(f"QwenCaptioner: Using attention implementation: {attnImplementation}")

            quantizationConfig = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            ) if self.device == "cuda" else None

            # Use AutoModelForImageTextToText with quantizationConfig
            QwenCaptioner._model = AutoModelForImageTextToText.from_pretrained(
                self.modelId, 
                torch_dtype=torch.float16, 
                device_map="auto" if self.device == "cuda" else None,
                quantization_config=quantizationConfig,
                attn_implementation=attnImplementation,
            )
            if self.device == "cpu":
                QwenCaptioner._model = QwenCaptioner._model.to(torch.float32) # Float32 for CPU usually safer/needed
            
            QwenCaptioner._processor = AutoProcessor.from_pretrained(self.modelId)
        
        self.model = QwenCaptioner._model
        self.processor = QwenCaptioner._processor
        self.device = self.model.device

    def _preprocessImage(self, imagePath: str, maxDim: int = 1024) -> Image.Image:
        img = Image.open(imagePath).convert("RGB")
        if max(img.size) > maxDim:
            img.thumbnail((maxDim, maxDim), Image.Resampling.LANCZOS)
        return img

    def generateCaption(self, imagePath: str) -> str:
        assert os.path.exists(imagePath), f"Path to image doesn't exist: {imagePath}"
        
        # Load and resize image to save VRAM
        img = self._preprocessImage(imagePath, maxDim=896)
        
        # Qwen-VL-utils process_vision_info accepts PIL images directly if we don't use file://
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": img},
                    {"type": "text", "text": "Describe this image in detail. Identify characters and unique features."},
                ],
            }
        ]
        
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        imageInputs, videoInputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=imageInputs,
            videos=videoInputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self.model.device)

        with torch.no_grad():
            generatedIds = self.model.generate(**inputs, max_new_tokens=128)
            
        generatedIdsTrimmed = [
            outIds[len(inIds) :] for inIds, outIds in zip(inputs.input_ids, generatedIds)
        ]
        outputText = self.processor.batch_decode(
            generatedIdsTrimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        
        # Cleanup
        del inputs
        del generatedIds
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        return outputText[0]

    def encodeImage(self, imagePath: str) -> list[float]:
        assert os.path.exists(imagePath), f"Path to image doesn't exist: {imagePath}"
        
        img = self._preprocessImage(imagePath, maxDim=896)
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": img},
                    {"type": "text", "text": "Extract features."},
                ],
            }
        ]
        
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        imageInputs, videoInputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=imageInputs,
            videos=videoInputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self.model.device)
        
        with torch.no_grad():
            gridThw = getattr(inputs, "image_grid_thw", None)
            outputs = self.model.visual(inputs.pixel_values, grid_thw=gridThw)
            embeddings = outputs[0].mean(dim=0).to(torch.float32)
            
        # Cleanup
        del inputs
        del outputs
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        return embeddings.cpu().numpy().tolist()

    def encodeText(self, text: str) -> list[float]:
        inputs = self.processor(text=[text], return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.model(input_ids=inputs.input_ids, attention_mask=inputs.attention_mask, output_hidden_states=True)
            lastHiddenState = outputs.last_hidden_state
            embeddings = lastHiddenState.mean(dim=1).squeeze(0).to(torch.float32)
            
        return embeddings.cpu().numpy().tolist()
