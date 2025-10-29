from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from models.base_models.model_interace import ModelInterface


class TranslateEnPt(ModelInterface):
    """

    """

    def __init__(self):
        """

        """
        tokenizer = AutoTokenizer.from_pretrained("unicamp-dl/translation-en-pt-t5")
        model = AutoModelForSeq2SeqLM.from_pretrained("unicamp-dl/translation-en-pt-t5")
        super().__init__(pipeline('text2text-generation', model=model, tokenizer=tokenizer))
