from abc import ABC, abstractmethod
from models.question import Question


class QuestionGenerator(ABC):
    def __init__(self, model: str):
        """

        """

        self._model = model

    @abstractmethod
    def generate(self, content: str, n_alternatives: int) -> Question:
        """

        :return:
        """
        pass

    @abstractmethod
    def evaluate_answer(self, question: Question, answer: int) -> str:
        """

        :return:
        """
        pass