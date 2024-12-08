import requests
from typing import Any, Dict
from openai import OpenAI
import json
from echolib.common.logger import logger
from .base import BaseModel
import time

class LMStudioModel(BaseModel):
    def __init__(self, api_url: str, headers: Dict[str, str], config: Dict[str, Any]) -> None:
        super().__init__(api_url, headers, config)
        self.client = OpenAI(base_url=api_url, api_key="not-needed")  # Adjust as needed
        logger.debug(f"Initialized LMStudioModel with api_url: {api_url}")

    def __str__(self) -> str:
        return "LMStudioModel"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(api_url={self.api_url})"

    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        try:
            with open(config_path, 'r') as file:
                config = json.load(file)
                logger.debug(f"Loaded config from {config_path}")
                return config
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}

    def generate_text(self, prompt: str, parameters: Dict[str, Any]) -> Any:
        data = {
            "messages": [
                {"role": "system", "content": parameters.get("instructions", "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful.")},
                {"role": "user", "content": prompt}
            ],
            "temperature": parameters.get("temperature", 0.7),
            "max_tokens": parameters.get("max_tokens", -1),
            "stream": parameters.get("stream", False)
        }
        logger.debug(f"Sending request to {self.api_url}/chat/completions with data: {data}")
        try:
            response = requests.post(f"{self.api_url}/chat/completions", headers=self.headers, json=data)
            response.raise_for_status()
            logger.debug(f"Received response: {response.json()}")
            return response.json()
        except Exception as e:
            logger.exception(f"Error during text generation: {e}")
            return {"error": str(e)}

    def predict(self, prompt: str, seed: int | None = None) -> Any:
        if seed is None:
            seed = int(time.time())
        logger.info(f"Predicting with prompt: {prompt[:20]}... and seed: {seed}")
        params = self.config.get('default_parameters', {})
        response = self.generate_text(prompt, params)
        return response

    def inference(self, prompt: str, seed: int | None = None) -> str:
        logger.info(f"Running inference with prompt: {prompt[:20]}...")
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt.strip()},
            ],
            model="local-model",  # Adjust if needed
            seed=seed
        )
        result = chat_completion.choices[0].message.content
        logger.debug(f"Inference result: {result}")
        return result

    def sys_inference(self, sys_prompt: str, usr_prompt: str, seed: int | None = None) -> str:
        logger.info(f"System inference with system prompt: {sys_prompt[:20]} and user prompt: {usr_prompt[:20]}")
        chat_completion = self.client.chat.completions.create(
            messages=[
                {"role": "assistant", "content": sys_prompt},
                {"role": "user", "content": usr_prompt.strip()},
            ],
            model="local-model",  # Adjust if needed
            temperature=0.7,
            seed=seed
        )
        result = chat_completion.choices[0].message.content
        logger.debug(f"System inference result: {result}")
        return result

    def interactive_prompt(self) -> None:
        logger.info("Starting interactive prompt session")
        print("You are now chatting with the intelligent assistant. Type something to start the conversation.")
        history = [
            {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
            {"role": "user", "content": "Hello, introduce yourself to someone opening this program for the first time. Be concise."},
        ]

        while True:
            try:
                chat_completion = self.client.chat.completions.create(
                    model="local-model",
                    messages=history,
                    temperature=0.7,
                    max_tokens=150,
                    stream=True
                )
                new_message = {"role": "assistant", "content": ""}
                for chunk in chat_completion:
                    if chunk.choices[0].delta.content:
                        print(chunk.choices[0].delta.content, end="", flush=True)
                        new_message["content"] += chunk.choices[0].delta.content
                history.append(new_message)
                print()
                user_input = input("> ")
                if user_input.lower() == 'quit':
                    logger.info("Exiting interactive prompt...")
                    print("Exiting interactive prompt...")
                    break
                history.append({"role": "user", "content": user_input})
            except KeyboardInterrupt:
                logger.info("Interactive prompt interrupted by user.")
                print("\nExiting interactive prompt...")
                break

    def update_token(self, new_token: str) -> None:
        self.headers['Authorization'] = f"Bearer {new_token}"
        logger.info("Token updated successfully!")

    def calc_tokens(self, prompt: str) -> int:
        num_tokens = len(prompt.split())
        logger.debug(f"Calculated {num_tokens} tokens for prompt: {prompt}")
        return num_tokens

    @classmethod
    def setup_from_config(cls, config_path: str) -> 'LMStudioModel':
        config = cls.load_config(config_path)
        api_url = config.get("api_url", "http://localhost:1234/v1")
        headers = {"Content-Type": "application/json"}
        headers.update(config.get("headers", {}))
        logger.info(f"Setting up LMStudioModel from config: {config_path}")
        return cls(api_url=api_url, headers=headers, config=config)

    @classmethod
    def setup_from_dict(cls, config_dict: Dict[str, Any]) -> 'LMStudioModel':
        api_url = config_dict.get("api_url", "http://localhost:1234/v1")
        headers = {"Content-Type": "application/json"}
        headers.update(config_dict.get("headers", {}))
        logger.info("Setting up LMStudioModel from dictionary config")
        return cls(api_url=api_url, headers=headers, config=config_dict)


if __name__ == '__main__':
    config_path = "models/configs/lm_studio.config.json"
    lm_studio = LMStudioModel.setup_from_config(config_path)
    result = lm_studio.sys_inference(sys_prompt="You are a helpful assistant", usr_prompt="Hello there", seed=42)
    logger.info(f"System inference result: {result}")
    print(result)
