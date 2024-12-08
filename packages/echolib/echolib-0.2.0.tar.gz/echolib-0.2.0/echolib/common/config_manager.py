# echolib/common/config_manager.py

from echolib.common.models import HFToken, ModelPreset, HFModel
from .logger import logger
import json
import os
from pathlib import Path
from appdirs import user_config_dir
from typing import Any, Dict, List, Optional

class ConfigManager:
    _instance = None

    def __new__(cls, config_dir: str = None):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, config_dir: str = None):
        if self._initialized:
            return
        self._initialized = True

        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            env_config_dir = os.getenv('ECHOLIB_CONFIG_DIR')
            if env_config_dir:
                self.config_dir = Path(env_config_dir)
            else:
                self.config_dir = Path(user_config_dir("echolib"))

        logger.info(f"Using configuration directory: {self.config_dir}")
        self.config_dir.mkdir(parents=True, exist_ok=True)

        self.tokens = self.load_tokens()
        self.presets = self.load_presets()
        self.hf_models = self.load_hf_models()
        self.lm_studio_config = self.load_lm_studio_config()

    def load_tokens(self) -> List[HFToken]:
        tokens_path = self.config_dir / 'tokens.json'
        if not tokens_path.exists():
            logger.error(f"tokens.json not found in {self.config_dir}. Please initialize your configuration.")
            return []
        try:
            with open(tokens_path, 'r') as file:
                tokens = json.load(file)
                assert len(tokens) > 0, "No tokens found in tokens.json."
                logger.info(f"Loaded {len(tokens)} tokens from {tokens_path}.")
                return [HFToken(**token) for token in tokens]
        except Exception as e:
            logger.error(f"Failed to load tokens from {tokens_path}: {e}")
            return []

    def load_presets(self) -> List[ModelPreset]:
        presets_path = self.config_dir / 'presets.json'
        if not presets_path.exists():
            logger.error(f"presets.json not found in {self.config_dir}. Please initialize your configuration.")
            return []
        try:
            with open(presets_path, 'r') as file:
                presets = json.load(file)
                assert len(presets) > 0, "No presets found in presets.json."
                logger.info(f"Loaded {len(presets)} presets from {presets_path}.")
                return [ModelPreset(**preset) for preset in presets]
        except Exception as e:
            logger.error(f"Failed to load presets from {presets_path}: {e}")
            return []

    def load_hf_models(self) -> List[HFModel]:
        hf_models_path = self.config_dir / 'hf_models.json'
        if not hf_models_path.exists():
            logger.error(f"hf_models.json not found in {self.config_dir}. Please initialize your configuration.")
            return []
        try:
            with open(hf_models_path, 'r') as file:
                hf_models = json.load(file)
                assert len(hf_models) > 0, "No HuggingFace models found in hf_models.json."
                logger.info(f"Loaded {len(hf_models)} HuggingFace models from {hf_models_path}.")
                return [HFModel(**model) for model in hf_models]
        except Exception as e:
            logger.error(f"Failed to load HuggingFace models from {hf_models_path}: {e}")
            return []

    def load_lm_studio_config(self) -> Optional[Dict[str, Any]]:
        lm_studio_path = self.config_dir / 'lm_studio.config.json'
        if not lm_studio_path.exists():
            logger.error(f"lm_studio.config.json not found in {self.config_dir}. Please initialize your configuration.")
            return None
        try:
            with open(lm_studio_path, 'r') as file:
                config = json.load(file)
                logger.info(f"Loaded LMStudio config from {lm_studio_path}.")
                return config
        except Exception as e:
            logger.error(f"Failed to load LMStudio config from {lm_studio_path}: {e}")
            return None

    def get_preset_by_id(self, preset_id: int) -> Optional[ModelPreset]:
        for preset in self.presets:
            if preset.id == preset_id:
                return preset
        logger.warning(f"Preset with ID {preset_id} not found.")
        return None

    def get_model_by_id(self, model_id: int) -> Optional[HFModel]:
        for model in self.hf_models:
            if model.id == model_id:
                return model
        logger.warning(f"Model with ID {model_id} not found.")
        return None

# Initialize ConfigManager singleton
config_manager = ConfigManager()
