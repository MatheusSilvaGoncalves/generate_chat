from models.base_models.t5_model import T5Model
from models.base_models.translate_en_pt import TranslateEnPt
from models.base_models.translate_pt_en import TranslatePtEn
from models.base_models.summarize_en import Summarize


def get_model(model_name: str):
    """

    :return:
    """

    if model_name == "t5":
        return T5Model()
    elif model_name == "pt-en":
        return TranslatePtEn()
    elif model_name == "en-pt":
        return TranslateEnPt()
    elif model_name == "summarize_en":
        return Summarize()
    else:
        raise NotImplementedError