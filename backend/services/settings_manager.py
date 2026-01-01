import json
import os
from pathlib import Path
from backend.utils.constants import DATA_DIR

class SettingsManager:
    _instance = None
    _configPath = DATA_DIR / "settings.json"
    
    DEFAULT_SETTINGS = {
        "activeModel": "Qwen3-VL-2B",
        "themeMode": "system"
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SettingsManager, cls).__new__(cls)
            cls._instance._settings = cls.DEFAULT_SETTINGS.copy()
            cls._instance._load()
        return cls._instance

    def _load(self):
        if self._configPath.exists():
            try:
                with open(self._configPath, "r") as f:
                    loaded = json.load(f)
                    self._settings.update(loaded)
            except Exception as e:
                print(f"Error loading settings: {e}")

    def save(self):
        try:
            with open(self._configPath, "w") as f:
                json.dump(self._settings, f, indent=4)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def get(self, key, default=None):
        return self._settings.get(key, default)

    def set(self, key, value):
        self._settings[key] = value
        self.save()
        
    @property
    def activeModel(self):
        return self.get("activeModel")
    
    @activeModel.setter
    def activeModel(self, value):
        self.set("activeModel", value)
