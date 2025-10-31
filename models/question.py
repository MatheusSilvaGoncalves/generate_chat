from dataclasses import dataclass


@dataclass
class Question:
    """
    Object that contains the content that describe a question:
                question: (str) with the question itself
                alternatives: (list[tuple[int, str]]) with possible answers (index and text)
                answer: (int) the correct answer to the question
    """

    question: str
    alternatives: list[tuple[int, str]]
    answer: int
