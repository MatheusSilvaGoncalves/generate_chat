from typing import Callable
from models.base_models.model_interace import ModelInterface


class Model:
    """

    """

    def __init__(self, model: ModelInterface, prompt_generator: Callable):
        """

        """

        self._model = model
        self._prompt_generator = prompt_generator

    def execute(self, content: list[str], kwargs: dict = None):
        """

        :return:
        """

        prompt = self._prompt_generator(content)

        return self._model.execute(prompt, kwargs)
