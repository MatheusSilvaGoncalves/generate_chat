import random
from models.question import Question
from models.prompts import Prompts
from models.model import Model
from models.base_models import TransformersModel
from models.base_models import TransformersAlternative


class QuestionGenerator:
    """
    Object that performs the complete workflow for generating a multiple choice question.
    """

    def __init__(self, model: dict, text: list[str], pt_en_pt: bool = True):
        """
        Initializes the object

        :param model: (dict) with the configuration of the workflow:
                "processing"
                "question", "correct_answer", "wrong_answer"
                Each item may have the following items:
                    "task": (str) with the task (e.g., "text2text-generation").
                    "name": (str) with the name of the model (e.g., "google/flan-t5-large").
                    "prompt": (str) with additional prompt.
                    "alternative": (bool) indicating whether to use the
                        TransformersModel or TransformersAlternative model.
                    "distractor": (bool) optional parameter indicating whether to use a
                        different section of text (useful for creating wrong answers)
                    "kwargs": (dict) with optional arguments of the model
                        (e.g., "max_new_tokens", "temperature").
        :param text: (list[str]) with the sections of the text.
        :param pt_en_pt: (bool) indicating whether to translate the workflow for english or not.
        """

        self._pt_en_pt = pt_en_pt
        self._text = text
        if pt_en_pt:
            pt_en_translator = TransformersAlternative('text2text-generation',
                                                       "unicamp-dl/translation-pt-en-t5")
            en_pt_translator = TransformersAlternative('text2text-generation',
                                                       "unicamp-dl/translation-en-pt-t5")
            self._pt_en_translator = Model(pt_en_translator, "", Prompts().prompt_factory("translate_pt_to", True))
            self._en_pt_translator = Model(en_pt_translator, "", Prompts().prompt_factory("translate_en_to", False))
        employed_models = {}
        self._workflow = {"processing": [], "question": [], "correct_answer": [], "wrong_answer": []}
        for key in self._workflow.keys():
            for step in model[key]:
                model_name = step["name"]
                model_task = step["task"]
                base_prompt = step.get("prompt", "")
                prompt = Prompts().prompt_factory(key, self._pt_en_pt)
                if model_name not in employed_models:
                    if "alternative" in step.keys():
                        employed_models[model_name] = TransformersAlternative(model_task, model_name)
                    else:
                        employed_models[model_name] = TransformersModel(model_task, model_name)
                item = {'model': Model(employed_models[model_name], base_prompt, prompt),
                        'kwargs': step.get("kwargs", {}), "distractor": step.get("distractor", False)}
                self._workflow[key].append(item)

    def generate(self, n_alternatives: int, debug: bool = True, max_tries: int = 5) -> Question:
        """
        Method that generates a complete multiple choice Question object.

        :param n_alternatives: (int) with the number of alternatives to be created.
        :param debug: (bool) indicating whether to show the intermediate steps or not.
        :param max_tries: (int) with maximum number of tries for generating different alternatives.

        :return: (Question) with the multiple choice question generated.
        """

        content = random.choice(self._text)
        section_number = content.split(" ")[0].rstrip(".")
        self._text.remove(content)
        original_content = content
        if self._pt_en_pt:
            content = self._pt_en_translator.execute([content])
        processed_content = content
        for item in self._workflow["processing"]:
            processed_content = item['model'].execute([processed_content], item['kwargs'])
        question_content = processed_content
        for item in self._workflow["question"]:
            question_content = item['model'].execute([question_content], item['kwargs'])
        item = self._workflow["correct_answer"][0]
        correct_answer_content = item['model'].execute([question_content, processed_content], item['kwargs'])
        answers = [correct_answer_content]
        if len(self._workflow["wrong_answer"]) != n_alternatives - 1:
            raise Exception(f"The number of provided models to generate wrong answers"
                            f"({len(self._workflow['wrong_answer'])}) is different of the desired ({n_alternatives - 1})")
        for item in self._workflow["wrong_answer"]:
            if item["distractor"]:
                acceptable_answer = False
                tries = 0
                while not acceptable_answer:
                    distractor = random.choice(self._text)
                    if self._pt_en_pt:
                        distractor = self._pt_en_translator.execute([distractor])

                    wrong_answer_content = item['model'].execute(
                        [question_content, correct_answer_content, distractor],
                        item['kwargs'])
                    if wrong_answer_content not in answers or tries > max_tries:
                        acceptable_answer = True
                    tries += 1
            else:
                wrong_answer_content = item['model'].execute([question_content, correct_answer_content, processed_content],
                                                             item['kwargs'])
            answers.append(wrong_answer_content)
        if self._pt_en_pt:
            question_content = f"{section_number}: {self._en_pt_translator.execute([question_content])}"
            new_answers = []
            for answer in answers:
                new_answers.append(self._en_pt_translator.execute([answer]))
            answers = new_answers
        else:
            question_content = f"{section_number}: {question_content}"

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
        Method that evaluates the answer for a given multiple choice question.

        :param question: (Question) with the multiple choice Question object.
        :param answer: (int) with the selected alternative
        :return: (tuple[str, int]) with the text assessing the answer's quality and the points made.
        """

        answers = question.alternatives
        correct_idx, correct_answer = [(i, answer) for i, (idx_original, answer)
                                       in enumerate(answers) if idx_original == question.answer][0]
        if correct_idx == answer:
            return "✅ Correto!", 1
        else:
            return f"❌ Errado! A resposta correta é: {correct_idx + 1}) {correct_answer}", 0
