from typing import Callable
from models.base_models.model_interace import ModelInterface


class Model:
    """
    Object that handles base models.
    """

    def __init__(self, model: ModelInterface, base_prompt: str, prompt_generator: Callable):
        """
        Initialize the object.

        :param model: (ModelInterface) object that executes the task.
        :param base_prompt: (str) with the base prompt.
        :param prompt_generator: (Callable) that includes additional info to the prompt
                (e.g., context, the question, correct answer, etc...).
        """

        self._model = model
        self._base_prompt = base_prompt
        self._prompt_generator = prompt_generator

    def execute(self, content: list[str], kwargs: dict = None) -> str:
        """
        Execute the pre-defined task.

        :param content: (list[str]) with the context (e.g., context, the question, correct answer, etc...).
        :param kwargs: (dict) with optional arguments (e.g., "max_new_tokens", "temperature").

        :return: (str) with the model's response.
        """

        prompt = self._prompt_generator(content)

        return self._model.execute(f"{self._base_prompt} {prompt}", kwargs)
