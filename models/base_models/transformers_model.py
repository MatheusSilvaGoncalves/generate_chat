from transformers import pipeline
from models.base_models.model_interace import ModelInterface


class TransformersModel(ModelInterface):
    """
    Transformers model.
    """

    def __init__(self, task: str, model: str):
        """
        Initialization of the object.

        :param task: (str) with the task (e.g., "text2text-generation").
        :param model: (str) with the model name (e.g., "google/flan-t5-large").
        """

        self._task = task
        super().__init__(pipeline(task, model=model))
