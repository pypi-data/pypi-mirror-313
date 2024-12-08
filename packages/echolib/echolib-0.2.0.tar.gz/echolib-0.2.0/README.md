# Run

make sure to have the following 3 files :
- `hf_models.json` 
```json
[
    {
        "id" : 1,
        "name" : "Mistral v0.2 ( HuggingFace )",
        "type" : "HUGGINGFACE",
        "kwargs" : {
            "api_url": "https://api-inference.huggingface.co/models",
            "headers": {
                "Authorization": "Bearer YOUR_API_KEY",
                "Content-Type": "application/json"
            },
            "model_huggingface_id": "mistralai/Mistral-7B-Instruct-v0.2",
            "default_parameters": {
                "max_length": -1,
                "max_new_tokens": 250,
                "temperature": 1e-8,
                "use_cache": true,
                "wait_for_model": true
            }
        },
        "preset" : 1
    },
    {
        "id" : 2,
        "name" : "Mistral v0.3 ( HuggingFace )",
        "type" : "HUGGINGFACE",
        "kwargs" : {
            "api_url": "https://api-inference.huggingface.co/models",
            "headers": {
                "Authorization": "Bearer YOUR_API_KEY",
                "Content-Type": "application/json"
            },
            "model_huggingface_id": "mistralai/Mistral-7B-Instruct-v0.3",
            "default_parameters": {
                "max_length": -1,
                "max_new_tokens": 250,
                "temperature": 1e-8,
                "use_cache": true,
                "wait_for_model": true
            }
        },
        "preset" : 1
    },
    {
        "id" : 3,
        "name" : "Phi 3 mini ( HuggingFace )",
        "type" : "HUGGINGFACE",
        "kwargs" : {
            "api_url": "https://api-inference.huggingface.co/models",
            "headers": {
                "Authorization": "Bearer YOUR_API_KEY",
                "Content-Type": "application/json"
            },
            "model_huggingface_id": "microsoft/Phi-3-mini-4k-instruct",
            "default_parameters": {
                "max_length": -1,
                "max_new_tokens": 250,
                "temperature": 1e-8,
                "use_cache": true,
                "wait_for_model": true
            }
        },
        "preset" : 2
    }
]
```
- `presets.json`
```json
[
    {
        "id" : 1,
        "name" : "Mistral Instruct",
        "input_prefix" : "[INST]",
        "input_suffix" : "[/INST]",
        "antiprompt" : "[INST]",
        "pre_prompt" : "",
        "pre_prompt_prefix" : "",
        "pre_prompt_suffix" : ""
    },
    {
        "id" : 2,
        "name" : "Phi 3",
        "input_prefix" : "<|user|>\n",
        "input_suffix" : "<|end|>\n<|assistant|>\n",
        "antiprompt" : "\"<|end|>\",  \"<|assistant|>\"",
        "pre_prompt" : "",
        "pre_prompt_prefix" : "<|end|>\n",
        "pre_prompt_suffix" : "<|system|>\n"
    }
]
```
- `tokens.json` : More tokens mean more reliability and fault tolerence, in my case I used 10 HuggingFace tokens.
```json
[
    {
        "id": 1,
        "name": "First",
        "value": "A HuggingFace api token"
    },
    {
        "id": 2,
        "name": "Second",
        "value": "Another token just to make sure the requests don't fail"
    },
    {
        "id": 3,
        "name": "Third",
        "value": "a third token as a backup"
    }
    ... Add more as needed
]
```

