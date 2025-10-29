from transformers import pipeline
from models.base_models.model_interace import ModelInterface


class TransformersModel(ModelInterface):
    """

    """

    def __init__(self, task: str, model: str):
        """

        """
        self._task = task

        super().__init__(pipeline(task, model=model))
