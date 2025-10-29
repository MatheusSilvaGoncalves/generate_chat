from abc import ABC


class ModelInterface(ABC):
    """

    """

    def __init__(self, model):
        """

        """

        self._model = model

    def execute(self, prompt: str, kwargs: dict = None) -> str:
        """

        :return:
        """

        if kwargs is None:
            kwargs = {}

        response = self._model(prompt, **kwargs)[0]
        if 'generated_text' in response.keys():
            return response['generated_text']
        else:
            return  response["summary_text"]
