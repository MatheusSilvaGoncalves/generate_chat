from transformers import pipeline
from models.base_models.model_interace import ModelInterface


class Summarize(ModelInterface):
    """

    """

    def __init__(self):
        """

        """

        super().__init__(pipeline("summarization", model="sshleifer/distilbart-cnn-12-6"))
