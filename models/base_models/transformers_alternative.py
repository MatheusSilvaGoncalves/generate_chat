from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from models.base_models.model_interace import ModelInterface


class TransformersAlternative(ModelInterface):
    """

    """

    def __init__(self, task: str, model: str):
        """

        """

        tokenizer = AutoTokenizer.from_pretrained(model)
        model_object = AutoModelForSeq2SeqLM.from_pretrained(model)
        super().__init__(pipeline(task, model=model_object, tokenizer=tokenizer))
