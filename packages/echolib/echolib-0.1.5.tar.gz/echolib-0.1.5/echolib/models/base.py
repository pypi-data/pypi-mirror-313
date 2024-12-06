from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseModel(ABC):
    """
    Abstract base class for models to interact with APIs and perform data processing.
    """

    def __init__(self, api_url: str, headers: Dict[str, str], config: Dict[str, Any]) -> None:
        self.api_url = api_url
        self.headers = headers
        self.config = config

    @staticmethod
    @abstractmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """
        Loads configuration from a specified path.
        """
        pass

    @abstractmethod
    def generate_text(self, prompt: str, parameters: Dict[str, Any]) -> Any:
        """
        Generates text based on a prompt and parameters.
        """
        pass

    @abstractmethod
    def predict(self, prompt: str, seed: int | None = None) -> Any:
        """
        Processes a prompt and returns a prediction.
        """
        pass

    @abstractmethod
    def inference(self, prompt: str, seed: int | None = None) -> str:
        """
        Performs inference using the model.
        """
        pass

    @abstractmethod
    def sys_inference(self, sys_prompt: str, usr_prompt: str, seed: int | None = None) -> str:
        """
        Performs inference using the model with system prompt.
        """
        pass

    @abstractmethod
    def update_token(self, new_token: str) -> None:
        """
        Updates the API token used for authentication.
        """
        pass

    @abstractmethod
    def calc_tokens(self, prompt: str) -> int:
        """
        Calculates the number of tokens in a prompt.
        """
        pass

    def interactive_prompt(self) -> None:
        """
        Optional: Implement an interactive prompt for testing purposes.
        """
        print("This method can be overridden by subclasses.")
