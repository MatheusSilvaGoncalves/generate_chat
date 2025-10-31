from typing import Callable


class Prompts:
    """
    Object that build the base prompts for each task in the workflow.
    """

    def prompt_factory(self, option: str, english: bool) -> Callable:
        """

        :param option: (str) with the type of task.
        :param english: (bool) indicating if the task is in english or portuguese.

        :return: (Callable) with the method to generate the prompt
        """

        if english:
            option = f"{option}_en"
        else:
            option = f"{option}_pt"

        if option == "correct_answer_en":
            return self.correct_answer_en
        elif option == "correct_answer_pt":
            return self.correct_answer_pt
        elif option == "wrong_answer_en":
            return self.wrong_answer_en
        elif option == "wrong_answer_pt":
            return self.wrong_answer_pt
        elif option == "question_en":
            return self.make_question_en
        elif option == "question_pt":
            return self.make_question_pt
        elif option == "processing_en":
            return self.summarize_en
        elif option == "processing_pt":
            return self.summarize_pt
        elif option == "translate_pt_to_en":
            return self.translate_pt_to_en
        elif option == "translate_en_to_pt":
            return self.translate_en_to_pt
        else:
            raise NotImplementedError

    @staticmethod
    def correct_answer_en(content: list[str]) -> str:
        """
        Prompt for generating a correct answer, in english.
        :param content: (list[str]) with the question and the text to extract the answer.

        :return: (str) with the prompt.
        """

        return f"""Text: {content[1]} \n Question: {content[0]}"""


    @staticmethod
    def correct_answer_pt(content: list[str]) -> str:
        """
        Prompt for generating a correct answer, in portuguese.
        :param content: (list[str]) with the question and the text to extract the answer.

        :return: (str) with the prompt.
        """

        return f"""Texto: {content[1]} \n Pergunta: {content[0]}"""


    @staticmethod
    def wrong_answer_en(content: list[str]) -> str:
        """
        Prompt for generating a wrong answer, in english.
        :param content: (list[str]) with the question, the correct answer, and the text to extract the answer.

        :return: (str) with the prompt.
        """

        return f"""Question: {content[0]} \n Correct answer: {content[1]} \n Context: {content[2]}"""


    @staticmethod
    def wrong_answer_pt(content: list[str]) -> str:
        """
        Prompt for generating a wrong answer, in portuguese.
        :param content: (list[str]) with the question, the correct answer, and the text to extract the answer.

        :return: (str) with the prompt.
        """

        return f"""Pergunta: {content[0]} \n Resposta correta: {content[1]} \n Contexto: {content[2]}"""


    @staticmethod
    def make_question_en(content: list[str]) -> str:
        """
        Prompt for generating a question, in english.
        :param content: (list[str]) with the text to extract the question.

        :return: (str) with the prompt.
        """

        return f"""Text: {content[0]} \n Question:"""

    @staticmethod
    def make_question_pt(content: list[str]) -> str:
        """
        Prompt for generating a question, in portuguese.
        :param content: (list[str]) with the text to extract the question.

        :return: (str) with the prompt.
        """

        return f"""Texto: {content[0]} \n Pergunta:"""

    @staticmethod
    def summarize_en(content: list[str]) -> str:
        """
        Prompt for summarizing a text, in english.
        :param content: (list[str]) with the text to summarize.

        :return: (str) with the prompt.
        """

        return content[0]


    @staticmethod
    def summarize_pt(content: list[str]) -> str:
        """
        Prompt for summarizing a text, in portuguese.
        :param content: (list[str]) with the text to summarize.

        :return: (str) with the prompt.
        """

        return content[0]


    @staticmethod
    def translate_en_to_pt(content: list[str]) -> str:
        """
        Prompt for translating a text, from english to portuguese.
        :param content: (list[str]) with the text to be translated.

        :return: (str) with the prompt.
        """

        return f"Translate English to Portuguese: {content[0]}."

    @staticmethod
    def translate_pt_to_en(content: list[str]) -> str:
        """
        Prompt for translating a text, from portuguese to english.
        :param content: (list[str]) with the text to be translated.

        :return: (str) with the prompt.
        """

        return f"Traduza do Português para o inglês: {content[0]}."
