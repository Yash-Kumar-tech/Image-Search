import torch
import gc
from backend.services.settings_manager import SettingsManager
from backend.models.qwen_captioner import QwenCaptioner
from backend.models.florence_captioner import FlorenceCaptioner

class ModelFactory:
    _instance = None
    _loadedModelName = None
    _activeModelInstance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelFactory, cls).__new__(cls)
            cls._instance.settings = SettingsManager()
        return cls._instance

    def getActiveModel(self):
        currentSetting = self.settings.activeModel
        
        # If we already have the right model loaded, return it
        if self._loadedModelName == currentSetting and self._activeModelInstance is not None:
            return self._activeModelInstance
            
        # Otherwise, unload previous if exists
        self.unloadModels()
        
        # Load new
        if currentSetting == "Florence-2-Base":
            self._activeModelInstance = FlorenceCaptioner()
        else:
            self._activeModelInstance = QwenCaptioner()
            
        self._loadedModelName = currentSetting
        return self._activeModelInstance

    def unloadModels(self):
        # This is a bit tricky with singletons, but we can try to clear class-level references
        QwenCaptioner._model = None
        QwenCaptioner._processor = None
        FlorenceCaptioner._model = None
        FlorenceCaptioner._processor = None
        
        self._activeModelInstance = None
        self._loadedModelName = None
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        gc.collect()
            
    def getModelName(self):
        return self.settings.activeModel
