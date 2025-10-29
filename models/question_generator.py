import random
from models.question import Question
from models.base_models import get_model
from models.prompts import Prompts
from models.model import Model
from models.base_models.transformers_model import TransformersModel


class QuestionGenerator:
    """

    """

    def __init__(self, model: dict, pt_en_pt: bool = True):
        """

        """

        self._pt_en_pt = pt_en_pt
        if pt_en_pt:
            translation_pt_en = get_model("pt-en")
            translation_en_pt = get_model("en-pt")
            self._pt_en_translator = Model(translation_pt_en, "", Prompts().prompt_factory("translate_pt_to", True))
            self._en_pt_translator = Model(translation_en_pt, "", Prompts().prompt_factory("translate_en_to", False))
        employed_models = {}
        self._workflow = {"processing": [], "question": [], "correct_answer": [], "wrong_answer": []}
        for key in self._workflow.keys():
            for step in model[key]:
                model_name = step["name"]
                model_task = step["task"]
                base_prompt = step.get("prompt", "")
                prompt = Prompts().prompt_factory(key, self._pt_en_pt)
                if model_name not in employed_models:
                    employed_models[model_name] = TransformersModel(model_task, model_name)
                item = {'model': Model(employed_models[model_name], base_prompt, prompt),
                        'kwargs': step.get("kwargs", {})}
                self._workflow[key].append(item)

    def generate(self, content: str, n_alternatives: int, debug=True):
        """

        """

        original_content = content
        if self._pt_en_pt:
            content = self._pt_en_translator.execute([content])
        processed_content = content
        for item in self._workflow["processing"]:
            processed_content = item['model'].execute(processed_content, item['kwargs'])
        question_content = processed_content
        for item in self._workflow["question"]:
            question_content = item['model'].execute(question_content, item['kwargs'])
        item = self._workflow["correct_answer"][0]
        correct_answer_content = item['model'].execute([question_content, processed_content], item['kwargs'])
        answers = [correct_answer_content]
        if len(self._workflow["wrong_answer"]) != n_alternatives - 1:
            raise Exception(f"The number of provided models to generate wrong answers"
                            f"({len(self._workflow['wrong_answer'])}) is different of the desired ({n_alternatives - 1})")
        for item in self._workflow["wrong_answer"]:
            wrong_answer_content = item['model'].execute([question_content, correct_answer_content, processed_content],
                                                         item['kwargs'])
            answers.append(wrong_answer_content)
        if self._pt_en_pt:
            question_content = self._en_pt_translator.execute([question_content])
            new_answers = []
            for answer in answers:
                new_answers.append(self._en_pt_translator.execute([answer]))
            answers = new_answers

        if debug:
            print("Original content: ", original_content)
            if self._pt_en_pt:
                print("Content translated to English: ", content)
            print("Processed content: ", processed_content)
            print("Question content: ", question_content)
            print("Correct answer content: ", correct_answer_content)
            for answer in answers:
                print("All answers: ", answer)

        indexed_answers = list(enumerate(answers))
        random.shuffle(indexed_answers)

        return Question(question_content, indexed_answers, 0)

    @staticmethod
    def evaluate_answer(question: Question, answer: int) -> tuple[str, int]:
        """

        :param question:
        :param answer:
        :return:
        """

        answers = question.alternatives
        correct_idx, correct_answer = [(i, answer) for i, (idx_original, answer)
                                       in enumerate(answers) if idx_original == question.answer][0]
        if correct_idx == answer:
            return "✅ Correto!", 1
        else:
            return f"❌ Errado! A resposta correta é: {correct_answer}", 0
