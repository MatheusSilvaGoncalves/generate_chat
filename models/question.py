from dataclasses import dataclass


@dataclass
class Question:
    """
    Object that
    """

    question: str
    alternatives: list[tuple[int, str]]
    answer: int
