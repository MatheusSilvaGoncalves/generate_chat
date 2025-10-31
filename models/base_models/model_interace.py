from abc import ABC
from transformers import Pipeline


class ModelInterface(ABC):
    """
    Interface class for base models.
    """

    def __init__(self, model: Pipeline):
        """
        Initialization of the class.

        :param model: (Pipeline) with the model pipeline.
        """

        self._model = model

    def execute(self, prompt: str, kwargs: dict = None) -> str:
        """
        Method that execute a given task.

        :param prompt: (str) with the prompt for the tas.
        :param kwargs: (dict) with optional arguments (e.g., "max_new_tokens", "temperature").

        :return: (str) with the model's response.
        """

        if kwargs is None:
            kwargs = {}

        response = self._model(prompt, **kwargs)[0]
        if 'generated_text' in response.keys():
            return response['generated_text']
        else:
            return  response["summary_text"]
