from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from models.base_models.model_interace import ModelInterface


class TransformersAlternative(ModelInterface):
    """
    Alternative Transformers model.
    """

    def __init__(self, task: str, model: str):
        """
        Initialization of the object.

        :param task: (str) with the task (e.g., "text2text-generation").
        :param model: (str) with the model name (e.g., "google/flan-t5-large").
        """

        tokenizer = AutoTokenizer.from_pretrained(model)
        model_object = AutoModelForSeq2SeqLM.from_pretrained(model)
        super().__init__(pipeline(task, model=model_object, tokenizer=tokenizer))
