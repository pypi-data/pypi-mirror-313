# echolib/models/model_manager.py

from typing import Any, Dict, Optional
from echolib.models.hf import HuggingFaceModel
from echolib.models.lm_studio import LMStudioModel
from echolib.common.config_manager import config_manager
from echolib.common.logger import logger

class ModelManager:
    def __init__(self):
        self.models: Dict[str, Any] = {}
        self.load_hf_models()
        self.load_lm_studio_models()

    def load_hf_models(self) -> None:
        for hf_model in config_manager.hf_models:
            if hf_model.type.upper() == "HUGGINGFACE":
                model = HuggingFaceModel.setup_from_dict(hf_model.kwargs)
                model.preset = config_manager.get_preset_by_id(hf_model.preset)
                self.models[hf_model.name] = model
                logger.debug(f"Loaded HuggingFace model: {hf_model.name}")

    def load_lm_studio_models(self) -> None:
        lm_studio_config = config_manager.lm_studio_config
        if lm_studio_config:
            lm_studio_model = LMStudioModel.setup_from_dict(lm_studio_config)
            self.models["LM Studio"] = lm_studio_model
            logger.debug("Loaded LMStudio model: LM Studio")
        else:
            logger.warning("LMStudio configuration is missing. Skipping LMStudio model.")

    def get_model(self, name: str) -> Optional[Any]:
        return self.models.get(name)

# Initialize ModelManager
model_manager = ModelManager()
