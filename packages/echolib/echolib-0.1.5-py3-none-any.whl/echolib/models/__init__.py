from .hf import HuggingFaceModel
from .lm_studio import LMStudioModel
from .base import BaseModel
from echolib.common import globals_, ModelPreset, logger
import os
from pathlib import Path

class AIModels:
    def __init__(self, config_dir: str = None) -> None:
        """
        Initialize AIModels by loading all configured models.

        Args:
            config_dir (str, optional): Path to the configuration directory.
                                        If None, uses the default from Globals.
        """
        self.models = {}
        self.config_dir = config_dir
        self.load_hf_models()
        self.load_lm_studio_models()

    def load_hf_models(self) -> None:
        for hf_model in globals_.hf_models:
            if hf_model.type.upper() == "HUGGINGFACE":
                model = HuggingFaceModel.setup_from_dict(hf_model.kwargs)
                model.preset = globals_.get_preset_by_id(hf_model.preset)
                self.models[hf_model.name] = model
                logger.debug(f"Loaded HuggingFace model: {hf_model.name}")

    def load_lm_studio_models(self) -> None:
        # Example: Load LMStudio models if any
        # Assuming similar configuration loading
        if self.config_dir:
            lm_studio_config_path = Path(self.config_dir) / 'lm_studio.config.json'
        else:
            lm_studio_config_path = Path(__file__).parent / 'configs' / 'lm_studio.config.json'
        
        if lm_studio_config_path.exists():
            lm_studio_model = LMStudioModel.setup_from_config(str(lm_studio_config_path))
            self.models["LM Studio"] = lm_studio_model
            logger.debug("Loaded LMStudio model: LM Studio")
        else:
            logger.warning(f"LMStudio config not found at {lm_studio_config_path}. Skipping LMStudio model.")

# Initialize AIModels with default configuration directory
ai_models = AIModels()
