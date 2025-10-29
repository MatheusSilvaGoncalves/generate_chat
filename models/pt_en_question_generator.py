import random
from models.question import Question
from models.question_interface import QuestionGenerator
from models.base_models import get_model
from models.prompts import Prompts
from models.model import Model


class PtEnQuestionGenerator(QuestionGenerator):
    """

    """

    def __init__(self, model: str):
        """

        """

        super().__init__(model)
        translation_pt_en = get_model("pt-en")
        translation_en_pt = get_model("en-pt")
        t5 = get_model("t5")
        summarize = get_model("summarize_en")
        self._pt_en_translator = Model(translation_pt_en, Prompts().prompt_factory("translate_pt_to_en"))
        self._en_pt_translator = Model(translation_en_pt, Prompts().prompt_factory("translate_en_to_pt"))
        self._make_question_en = Model(t5, Prompts().prompt_factory("make_question_en"))
        self._summarize_en = Model(summarize, Prompts().prompt_factory("summarize_en"))
        self._correct_answer = Model(t5, Prompts().prompt_factory("correct_en"))
        self._wrong_answer = Model(t5, Prompts().prompt_factory("wrong_en"))

    def generate(self, content: str, n_alternatives: int, debug=True):
        """

        """

        english_content = self._pt_en_translator.execute([content])
        summarized = self._summarize_en.execute([english_content])
        english_question = self._make_question_en.execute([summarized])
        correct_answer = self._correct_answer.execute([english_question, english_content])
        portuguese_question = self._en_pt_translator.execute([english_question])
        portuguese_answer = self._en_pt_translator.execute([correct_answer])
        answers = [portuguese_answer]
        for _ in range(n_alternatives - 1):
            kwargs = {"max_new_tokens": 100, "temperature": 0.5 + random.random(), "top_k": 50}
            wrong_answer = self._wrong_answer.execute([english_question, correct_answer, english_content], kwargs)
            answers.append(self._en_pt_translator.execute([wrong_answer]))

        if debug:
            print("Original content: ", content)
            print("Content translated to English: ", english_content)
            print("Summarized content: ", summarized)
            print("English Question: ", english_question)
            print("English Correct Answer: ", correct_answer)
            for answer in answers:
                print("Portuguese answers: ", answer)

        indexed_answers = list(enumerate(answers))
        random.shuffle(indexed_answers)

        return Question(portuguese_question, indexed_answers, 0)

    def evaluate_answer(self, question: Question, answer: int) -> tuple[str, int]:
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
