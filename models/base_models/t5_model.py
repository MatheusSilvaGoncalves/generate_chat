from transformers import pipeline
from models.base_models.model_interace import ModelInterface


class T5Model(ModelInterface):
    """

    """

    def __init__(self):
        """

        """

        super().__init__(pipeline("text2text-generation", model="google/flan-t5-base"))
