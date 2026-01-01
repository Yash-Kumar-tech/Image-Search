from transformers import AutoModelForImageTextToText, AutoProcessor, BitsAndBytesConfig
from transformers.utils import is_flash_attn_2_available
from qwen_vl_utils import process_vision_info
from PIL import Image
import os
import torch

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
            self.model_id = "Qwen/Qwen3-VL-2B-Instruct"
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"QwenCaptioner: Using device: {self.device}")
            
            attn_implementation = "flash_attention_2" if is_flash_attn_2_available() else "sdpa"
            print(f"QwenCaptioner: Using attention implementation: {attn_implementation}")

            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            ) if self.device == "cuda" else None

            # Use AutoModelForImageTextToText with quantization_config
            QwenCaptioner._model = AutoModelForImageTextToText.from_pretrained(
                self.model_id, 
                torch_dtype=torch.float16, 
                device_map="auto" if self.device == "cuda" else None,
                quantization_config=quantization_config,
                attn_implementation=attn_implementation,
            )
            if self.device == "cpu":
                QwenCaptioner._model = QwenCaptioner._model.to(torch.float32) # Float32 for CPU usually safer/needed
            
            QwenCaptioner._processor = AutoProcessor.from_pretrained(self.model_id)
        
        self.model = QwenCaptioner._model
        self.processor = QwenCaptioner._processor
        self.device = self.model.device

    def generateCaption(self, imagePath: str) -> str:
        assert os.path.exists(imagePath), f"Path to image doesn't exist: {imagePath}"
        
        # Standard Qwen-VL chat message structure
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": f"file://{imagePath}"},
                    {"type": "text", "text": "Describe this image in detail."},
                ],
            }
        ]
        
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self.model.device)

        generated_ids = self.model.generate(**inputs, max_new_tokens=128)
        generated_ids_trimmed = [
            out_ids[len(in_ids) :] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        output_text = self.processor.batch_decode(
            generated_ids_trimmed, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        return output_text[0]

    def encodeImage(self, imagePath: str) -> list[float]:
        assert os.path.exists(imagePath), f"Path to image doesn't exist: {imagePath}"
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "image": f"file://{imagePath}"},
                    {"type": "text", "text": "Extract features."},
                ],
            }
        ]
        
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt",
        )
        inputs = inputs.to(self.model.device)
        
        with torch.no_grad():
            # Extract visual features from the vision tower
            # For Qwen3-VL, the processor returns 'image_grid_thw'
            grid_thw = getattr(inputs, "image_grid_thw", None)
            outputs = self.model.visual(inputs.pixel_values, grid_thw=grid_thw)
            # Global average pooling on the hidden states
            embeddings = outputs[0].mean(dim=0).to(torch.float32)
            
        return embeddings.cpu().numpy().tolist()

    def encodeText(self, text: str) -> list[float]:
        inputs = self.processor(text=[text], return_tensors="pt").to(self.model.device)
        
        with torch.no_grad():
            outputs = self.model.model(input_ids=inputs.input_ids, attention_mask=inputs.attention_mask, output_hidden_states=True)
            last_hidden_state = outputs.last_hidden_state
            # Mean pooling across sequence tokens
            embeddings = last_hidden_state.mean(dim=1).squeeze(0).to(torch.float32)
            
        return embeddings.cpu().numpy().tolist()
