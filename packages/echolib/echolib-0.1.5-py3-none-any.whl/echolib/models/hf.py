import re
import requests
import json
from typing import Any, Dict
from transformers import PreTrainedTokenizerFast
from echolib.common import globals_, HFToken, ModelPreset
from echolib.common.logger import logger
from .base import BaseModel

class HuggingFaceModel(BaseModel):
    def __init__(self, api_url: str, headers: Dict[str, str], config: Dict[str, Any], preset: ModelPreset | None = None, load_tokenizer: bool = False) -> None:
        super().__init__(api_url, headers, config)
        self.model_id = config.get('model_huggingface_id')
        self.api_url = f"{api_url}/{self.model_id}"
        self.hf_tokens: list[HFToken] = globals_.load_tokens()
        self.current_token_index = 0
        self.exhausted_tokens = set()
        self.update_token(self.hf_tokens[self.current_token_index].value)
        if load_tokenizer:
            self.tokenizer = PreTrainedTokenizerFast.from_pretrained(self.model_id)
        else:
            self.tokenizer = None
        self.preset: ModelPreset | None = preset
        self.max_iterations = 10
        logger.debug(f"Initialized HuggingFaceModel with model_id: {self.model_id}, api_url: {self.api_url}, load_tokenizer: {load_tokenizer}")
        logger.info(f"Initialized HuggingFaceModel with model_id: {self.model_id}, api_url: {self.api_url}, load_tokenizer: {load_tokenizer}")

    def __str__(self) -> str:
        return "HuggingFaceModel"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model_id={self.model_id})"

    def get_preset(self) -> ModelPreset | None:
        return self.preset

    def get_input_prefix(self) -> str:
        return self.preset.input_prefix if self.preset else ""

    def get_input_suffix(self) -> str:
        return self.preset.input_suffix if self.preset else ""

    def get_pre_prompt(self) -> str:
        return self.preset.pre_prompt if self.preset else ""

    def get_pre_prompt_prefix(self) -> str:
        return self.preset.pre_prompt_prefix if self.preset else ""

    def get_pre_prompt_suffix(self) -> str:
        return self.preset.pre_prompt_suffix if self.preset else ""

    def set_max_iterations(self, max_iterations: int) -> None:
        self.max_iterations = max_iterations
        logger.debug(f"Set max iterations to: {max_iterations}")

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

    def preprocess_messages(self, messages: list) -> str:
        context = ""
        for message in messages:
            role = message['role']
            content = message['content']
            context += f"{role}: {content}\n"
        return context

    def query(self, payload: Dict[str, Any]) -> Any:
        logger.debug("Fetching all tokens")
        self.hf_tokens = globals_.load_tokens()
        logger.debug(f"Querying API with payload: {payload}")
        response = requests.post(self.api_url, headers=self.headers, json=payload, stream=True)
        result = ""
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    result += decoded_line
            logger.debug(f"Received response: {result}")
            return json.loads(result)
        elif response.status_code in [429, 400]:  # Rate limit reached or token invalid
            logger.warning("Rate limit reached or token invalid, rotating token.")
            self.exhausted_tokens.add(self.current_token_index)
            if len(self.exhausted_tokens) >= len(self.hf_tokens):
                logger.error("All tokens have been exhausted. Please wait before retrying.")
                raise Exception("All tokens have been exhausted. Please wait before retrying.")
            self.rotate_token()
            return self.query(payload)  # Retry with new token
        else:
            logger.error(f"Failed to fetch models. Status code: {response.status_code}, Response: {response.text}")
            raise Exception(f"Failed to fetch models. Status code: {response.status_code}\nResponse: {response.text}")

    def generate_text(self, prompt: str, parameters: Dict[str, Any]) -> Any:
        logger.info(f"Generating text with prompt: {prompt[:20]}... and parameters: {parameters}")
        payload = {
            "inputs": prompt,
            **parameters
        }
        try:
            response = self.query(payload)
            if isinstance(response, list):
                response = response.pop()
            response['error'] = False
            response['message'] = "Success"
            logger.debug(f"Generated response: {response}")
            return response
        except Exception as e:
            logger.exception(f"Error during text generation: {e}")
            return {'error': True, 'message': str(e)}

    def extract_assistant_response(self, generated_text: str) -> str:
        pattern = re.compile(r"assistant:\s*(.*)", re.IGNORECASE)
        match = pattern.search(generated_text)
        if match:
            return match.group(1).strip()
        else:
            return generated_text.strip()

    def predict(self, prompt: str, seed: int | None = None) -> Any:
        logger.info(f"Predicting with prompt: {prompt[:20]}...")
        params = self.config.get('default_parameters', {}).copy()
        if seed is not None:
            params["seed"] = seed
        initial_context = prompt
        context = initial_context
        iteration = 0
        while True:
            logger.debug(f"Starting iteration: {iteration}")
            generated_text_array = self.generate_text(context, params)
            if generated_text_array.get("error"):
                logger.error(f"Error in generated text array: {generated_text_array}")
                return {
                    'generated_text': f"Error (Not HuggingFace Generated): {generated_text_array.get('message')}",
                    'error': True,
                }
            generated_text = generated_text_array.get("generated_text", "")
            new_content = generated_text[len(context):]
            if not new_content.strip() or new_content in context:
                break
            context += new_content
            iteration += 1
            if iteration > self.max_iterations:
                break
        context = context[len(initial_context):]
        assistant_response = self.extract_assistant_response(context)
        logger.debug(f"Final assistant response: {assistant_response}")
        return {
            'generated_text': assistant_response,
            'error': False
        }

    def inference(self, prompt: str, seed: int | None = None) -> str:
        logger.info(f"Running inference with prompt: {prompt[:20]}...")
        generated_text = self.predict(prompt=prompt, seed=seed)
        if generated_text.get("error"):
            logger.error(f"Inference error: {generated_text.get('generated_text')}")
            return generated_text.get("generated_text")
        return generated_text.get("generated_text")

    def wrap_prompt(self, prompt: str, role: str) -> str:
        return f"{prompt}"

    def sys_inference(self, sys_prompt: str, usr_prompt: str, seed: int | None = None) -> str:
        logger.info(f"System inference with system prompt: {sys_prompt[:20]}, user prompt: {usr_prompt[:20]}")
        prompt = f'''{self.get_input_prefix()}system: {self.wrap_prompt(sys_prompt.strip(), role="system")}\nuser: {self.wrap_prompt(usr_prompt.strip(), role="user")}\n{self.get_input_suffix()}'''
        if self.get_pre_prompt():
            prompt = f"{self.get_pre_prompt_prefix()}{self.get_pre_prompt()}{self.get_pre_prompt_suffix()}\n{prompt}"
        return self.inference(prompt=prompt, seed=seed)

    def inference_with_tokens(self, prompt: str, max_new_tokens: int = 2) -> str:
        logger.info(f"Running inference with prompt: {prompt[:20]}... and max_new_tokens: {max_new_tokens}")
        params = self.config.get('default_parameters', {}).copy()
        params["max_new_tokens"] = max_new_tokens
        generated_text = self.generate_text(prompt, params)
        if generated_text.get("error"):
            logger.error(f"Inference error: {generated_text.get('message')}")
            return generated_text.get("message")
        return generated_text.get("generated_text", "")

    def rotate_token(self):
        starting_index = self.current_token_index
        while True:
            self.current_token_index = (self.current_token_index + 1) % len(self.hf_tokens)
            if self.current_token_index == starting_index:
                break
            if self.current_token_index not in self.exhausted_tokens:
                new_token = self.hf_tokens[self.current_token_index].value
                self.update_token(new_token)
                logger.info(f"Rotated to new token. Index: {self.current_token_index}")
                return
        logger.error("All tokens have been exhausted. Please wait before retrying.")
        raise Exception("All tokens have been exhausted. Please wait before retrying.")

    def update_token(self, new_token: str) -> None:
        self.headers['Authorization'] = f"Bearer {new_token}"
        logger.info("Token updated successfully!")

    def load_tokenizer_with_rotation(self, reload: bool = False):
        starting_index = self.current_token_index
        while True:
            token = self.hf_tokens[self.current_token_index].value
            try:
                logger.info(f"Attempting to load tokenizer for model: {self.model_id} with token index: {self.current_token_index}")
                self.tokenizer = PreTrainedTokenizerFast.from_pretrained(self.model_id, use_auth_token=token)
                logger.info(f"Successfully loaded tokenizer for model: {self.model_id}")
                return self.tokenizer
            except Exception as e:
                logger.warning(f"Failed to load tokenizer with token index: {self.current_token_index}, error: {e}")
                self.exhausted_tokens.add(self.current_token_index)
                self.rotate_token()
                if self.current_token_index == starting_index:
                    logger.error("All tokens have been exhausted. Please wait before retrying.")
                    raise Exception("All tokens have been exhausted. Please wait before retrying.")

    def calc_tokens(self, prompt: str) -> int:
        if not self.tokenizer:
            self.load_tokenizer_with_rotation()
        encoded_inputs = self.tokenizer(prompt)
        token_count = len(encoded_inputs['input_ids'])
        logger.debug(f"Calculated tokens: {token_count} for prompt: {prompt}")
        return token_count

    @classmethod
    def setup_from_config(cls, config_path: str) -> 'HuggingFaceModel':
        config = cls.load_config(config_path)
        api_url = config["api_url"]
        headers = config.get("headers", {})
        logger.info(f"Setting up HuggingFaceModel from config: {config_path}")
        return cls(api_url=api_url, headers=headers, config=config)

    @classmethod
    def setup_from_dict(cls, config_dict: Dict[str, Any]) -> 'HuggingFaceModel':
        api_url = config_dict.get("api_url")
        headers = config_dict.get("headers", {})
        logger.info("Setting up HuggingFaceModel from dictionary config")
        return cls(api_url=api_url, headers=headers, config=config_dict)

if __name__ == '__main__':
    config_path = "models/configs/huggingface.config.json"
    hf_model = HuggingFaceModel.setup_from_config(config_path)
    sys_msg = "You are a helpful coding assistant that gives correct code."
    usr_msg = "Give me a fibonacci function using Rust, write the response in a code block"
    result = hf_model.sys_inference(sys_prompt=sys_msg, usr_prompt=usr_msg)
    logger.info(f"System inference result: {result}")
    print(result)
