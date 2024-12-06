import unittest
from unittest.mock import patch, MagicMock
from echolib.models.hf import HuggingFaceModel
from echolib.models.lm_studio import LMStudioModel
from echolib.common.models import HFToken, ModelPreset

class TestHuggingFaceModel(unittest.TestCase):

    @patch('echolib.models.hf.requests.post')
    def test_generate_text_success(self, mock_post):
        # Mock a successful HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = [b'{"generated_text": "Hello world"}']
        mock_post.return_value = mock_response

        # Initialize the model with mock configurations
        config = {
            "model_huggingface_id": "mock/model-id",
            "default_parameters": {
                "max_new_tokens": 10
            }
        }
        model = HuggingFaceModel(
            api_url="https://api-inference.huggingface.co/models",
            headers={"Authorization": "Bearer mock_token"},
            config=config
        )

        # Call generate_text
        response = model.generate_text("Test prompt", {"max_new_tokens": 10})

        # Assertions
        self.assertIn("generated_text", response)
        self.assertFalse(response["error"])
        self.assertEqual(response["generated_text"], "Hello world")

    @patch('echolib.models.hf.requests.post')
    def test_generate_text_failure(self, mock_post):
        # Mock a failed HTTP response (e.g., Internal Server Error)
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        # Initialize the model with mock configurations
        config = {
            "model_huggingface_id": "mock/model-id",
            "default_parameters": {
                "max_new_tokens": 10
            }
        }
        model = HuggingFaceModel(
            api_url="https://api-inference.huggingface.co/models",
            headers={"Authorization": "Bearer mock_token"},
            config=config
        )

        # Call generate_text
        response = model.generate_text("Test prompt", {"max_new_tokens": 10})

        # Assertions
        self.assertIn("error", response)
        self.assertTrue(response["error"])
        self.assertIn("Failed to fetch models", response["message"])

    @patch('echolib.models.hf.requests.post')
    def test_generate_text_rate_limit(self, mock_post):
        # Mock a rate-limited HTTP response
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.text = "Rate limit exceeded"
        mock_post.return_value = mock_response

        # Initialize the model with mock configurations
        config = {
            "model_huggingface_id": "mock/model-id",
            "default_parameters": {
                "max_new_tokens": 10
            }
        }
        model = HuggingFaceModel(
            api_url="https://api-inference.huggingface.co/models",
            headers={"Authorization": "Bearer mock_token_1"},
            config=config
        )

        # Add a second token for rotation
        model.hf_tokens = [
            HFToken(id=1, name="Token1", value="mock_token_1"),
            HFToken(id=2, name="Token2", value="mock_token_2")
        ]

        # Call generate_text, expecting token rotation and eventual exhaustion
        response = model.generate_text("Test prompt", {"max_new_tokens": 10})

        # Assertions
        self.assertIn("error", response)
        self.assertTrue(response["error"])
        self.assertIn("All tokens have been exhausted. Please wait before retrying.", response["message"])

class TestLMStudioModel(unittest.TestCase):

    @patch('echolib.models.lm_studio.OpenAI')
    def test_sys_inference_success(self, mock_openai):
        # Mock the OpenAI client
        mock_client_instance = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock(message=MagicMock(content="Hello from LM Studio"))]
        mock_client_instance.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client_instance

        # Initialize the model with mock configurations
        config = {
            "api_url": "http://localhost:1234/v1",
            "default_parameters": {
                "temperature": 0.7,
                "max_tokens": 10,
                "stream": False
            }
        }
        model = LMStudioModel(
            api_url="http://localhost:1234/v1",
            headers={"Content-Type": "application/json"},
            config=config
        )

        # Call sys_inference
        response = model.sys_inference(
            sys_prompt="You are a helpful assistant.",
            usr_prompt="Hello there",
            seed=42
        )

        # Assertions
        self.assertEqual(response, "Hello from LM Studio")
        mock_openai.assert_called_once_with(base_url="http://localhost:1234/v1", api_key="not-needed")
        mock_client_instance.chat.completions.create.assert_called_once()

    @patch('echolib.models.lm_studio.OpenAI')
    def test_sys_inference_failure(self, mock_openai):
        # Mock the OpenAI client to raise an exception
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.side_effect = Exception("Internal Server Error")
        mock_openai.return_value = mock_client_instance

        # Initialize the model with mock configurations
        config = {
            "api_url": "http://localhost:1234/v1",
            "default_parameters": {
                "temperature": 0.7,
                "max_tokens": 10,
                "stream": False
            }
        }
        model = LMStudioModel(
            api_url="http://localhost:1234/v1",
            headers={"Content-Type": "application/json"},
            config=config
        )

        # Call sys_inference and expect an exception
        with self.assertRaises(Exception) as context:
            model.sys_inference(
                sys_prompt="You are a helpful assistant.",
                usr_prompt="Hello there",
                seed=42
            )

        # Assertions
        self.assertTrue("Internal Server Error" in str(context.exception))
        mock_openai.assert_called_once_with(base_url="http://localhost:1234/v1", api_key="not-needed")
        mock_client_instance.chat.completions.create.assert_called_once()

    @patch('echolib.models.lm_studio.OpenAI')
    def test_inference_success(self, mock_openai):
        # Mock the OpenAI client for inference
        mock_client_instance = MagicMock()
        mock_completion = MagicMock()
        mock_completion.choices = [MagicMock(message=MagicMock(content="Morocco gained independence on November 18, 1956."))]
        mock_client_instance.chat.completions.create.return_value = mock_completion
        mock_openai.return_value = mock_client_instance

        # Initialize the model with mock configurations
        config = {
            "api_url": "http://localhost:1234/v1",
            "default_parameters": {
                "temperature": 0.7,
                "max_tokens": 10,
                "stream": False
            }
        }
        model = LMStudioModel(
            api_url="http://localhost:1234/v1",
            headers={"Content-Type": "application/json"},
            config=config
        )

        # Call inference
        response = model.inference(
            prompt="What's the independence date of Morocco?",
            seed=42
        )

        # Assertions
        self.assertEqual(response, "Morocco gained independence on November 18, 1956.")
        mock_openai.assert_called_once_with(base_url="http://localhost:1234/v1", api_key="not-needed")
        mock_client_instance.chat.completions.create.assert_called_once()

    @patch('echolib.models.lm_studio.OpenAI')
    def test_inference_failure(self, mock_openai):
        # Mock the OpenAI client to raise an exception
        mock_client_instance = MagicMock()
        mock_client_instance.chat.completions.create.side_effect = Exception("Internal Server Error")
        mock_openai.return_value = mock_client_instance

        # Initialize the model with mock configurations
        config = {
            "api_url": "http://localhost:1234/v1",
            "default_parameters": {
                "temperature": 0.7,
                "max_tokens": 10,
                "stream": False
            }
        }
        model = LMStudioModel(
            api_url="http://localhost:1234/v1",
            headers={"Content-Type": "application/json"},
            config=config
        )

        # Call inference and expect an exception
        with self.assertRaises(Exception) as context:
            model.inference(
                prompt="What's the independence date of Morocco?",
                seed=42
            )

        # Assertions
        self.assertTrue("Internal Server Error" in str(context.exception))
        mock_openai.assert_called_once_with(base_url="http://localhost:1234/v1", api_key="not-needed")
        mock_client_instance.chat.completions.create.assert_called_once()

    # Removed test_generate_text_rate_limit for LMStudioModel as it does not apply

if __name__ == '__main__':
    unittest.main()
