from echolib.common.models import HFToken, ModelPreset, HFModel
from .logger import logger
import json
import os
from pathlib import Path

class Globals:
    def __init__(self, config_dir: str = None):
        """
        Initialize Globals with a configuration directory.

        Args:
            config_dir (str, optional): Path to the configuration directory.
                                         If None, checks the ECHOLIB_CONFIG_DIR environment variable.
                                         If still None, defaults to the 'configs' directory outside the package.
        """
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            # Check environment variable
            env_config_dir = os.getenv('ECHOLIB_CONFIG_DIR')
            if env_config_dir:
                self.config_dir = Path(env_config_dir)
            else:
                # Default to user's config directory
                from appdirs import user_config_dir
                default_dir = Path(user_config_dir("echolib"))
                self.config_dir = default_dir

        logger.info(f"Using configuration directory: {self.config_dir}")

        self.tokens = self.load_tokens()
        self.presets = self.load_presets()
        self.hf_models = self.load_hf_models()

    def load_tokens(self) -> list[HFToken]:
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

    def load_presets(self) -> list[ModelPreset]:
        presets_path = self.config_dir / 'presets.json'
        try:
            with open(presets_path, 'r') as file:
                presets = json.load(file)
                assert len(presets) > 0, "No presets found in presets.json."
                logger.info(f"Loaded {len(presets)} presets from {presets_path}.")
                return [ModelPreset(**preset) for preset in presets]
        except Exception as e:
            logger.error(f"Failed to load presets from {presets_path}: {e}")
            return []

    def load_hf_models(self) -> list[HFModel]:
        hf_models_path = self.config_dir / 'hf_models.json'
        try:
            with open(hf_models_path, 'r') as file:
                hf_models = json.load(file)
                assert len(hf_models) > 0, "No HuggingFace models found in hf_models.json."
                logger.info(f"Loaded {len(hf_models)} HuggingFace models from {hf_models_path}.")
                return [HFModel(**model) for model in hf_models]
        except Exception as e:
            logger.error(f"Failed to load HuggingFace models from {hf_models_path}: {e}")
            return []

    def get_preset_by_id(self, preset_id: int) -> ModelPreset:
        for preset in self.presets:
            if preset.id == preset_id:
                return preset
        logger.warning(f"Preset with ID {preset_id} not found.")
        return None

    def get_model_by_id(self, model_id: int) -> HFModel:
        for model in self.hf_models:
            if model.id == model_id:
                return model
        logger.warning(f"Model with ID {model_id} not found.")
        return None

# Initialize Globals with default config directory
globals_ = Globals()
