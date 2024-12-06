class HFToken:
    def __init__(self, id: int, name: str, value: str) -> None:
        """
        Represents a token in the Hugging Face model.

        Args:
            id (int): The unique identifier for the token.
            name (str): The name of the token.
            value (str): The value of the token.
        """
        self.id = id
        self.name = name
        self.value = value

    def __repr__(self) -> str:
        return f"HFToken(id={self.id}, name='{self.name}', value='***')"

class ModelPreset:
    def __init__(
        self, 
        id: int, 
        name: str,
        input_prefix: str,
        input_suffix: str,
        antiprompt: str,
        pre_prompt: str,
        pre_prompt_prefix: str,
        pre_prompt_suffix: str,
    ) -> None:
        """
        Represents a preset configuration for a model.

        Args:
            id (int): The unique identifier for the preset.
            name (str): The name of the preset.
            input_prefix (str): The prefix for input.
            input_suffix (str): The suffix for input.
            antiprompt (str): The antiprompt string.
            pre_prompt (str): The pre-prompt string.
            pre_prompt_prefix (str): The prefix for the pre-prompt.
            pre_prompt_suffix (str): The suffix for the pre-prompt.
        """
        self.id = id
        self.name = name
        self.input_prefix = input_prefix
        self.input_suffix = input_suffix
        self.antiprompt = antiprompt
        self.pre_prompt = pre_prompt
        self.pre_prompt_prefix = pre_prompt_prefix
        self.pre_prompt_suffix = pre_prompt_suffix

    def __repr__(self) -> str:
        return (
            f"ModelPreset(id={self.id}, name='{self.name}')"
        )

class HFModel:
    def __init__(
        self,
        id: int,
        name: str,
        type: str,
        kwargs: dict,
        preset: int
    ) -> None:
        """
        Represents a Hugging Face model configuration.

        Args:
            id (int): The unique identifier for the model.
            name (str): The name of the model.
            type (str): The type of the model.
            kwargs (dict): Additional keyword arguments for the model.
            preset (int): The preset ID associated with the model.
        """
        self.id = id
        self.name = name
        self.type = type
        self.kwargs = kwargs
        self.preset = preset

    def __repr__(self) -> str:
        return (
            f"HFModel(id={self.id}, name='{self.name}', type='{self.type}', preset={self.preset})"
        )
