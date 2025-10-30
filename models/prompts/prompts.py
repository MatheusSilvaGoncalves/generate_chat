class Prompts:
    """

    """

    def prompt_factory(self, option: str, english: bool):
        """

        :param option:
        :return:
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

        """

        return f"""Text: {content[1]} \n Question: {content[0]}"""


    @staticmethod
    def correct_answer_pt(content: list[str]) -> str:
        """

        """

        return f"""Texto: {content[1]} \n Pergunta: {content[0]}"""


    @staticmethod
    def wrong_answer_en(content: list[str]) -> str:
        """

        """

        return f"""Question: {content[0]} \n Correct answer: {content[1]} \n Context: {content[2]}"""


    @staticmethod
    def wrong_answer_pt(content: list[str]) -> str:
        """

        """

        return f"""Pergunta: {content[0]} \n Resposta correta: {content[1]} \n Contexto: {content[2]}"""


    @staticmethod
    def make_question_en(content: list[str]) -> str:
        """

        """

        return f"""Text: {content[0]} \n Question:"""

    @staticmethod
    def make_question_pt(content: list[str]) -> str:
        """

        """

        return f"""Texto: {content[0]} \n Pergunta:"""

    @staticmethod
    def summarize_en(content: list[str]) -> str:
        """

        """

        return content[0]


    @staticmethod
    def summarize_pt(content: list[str]) -> str:
        """

        """

        return content[0]


    @staticmethod
    def translate_en_to_pt(content: list[str]) -> str:
        """

        """

        return f"Translate English to Portuguese: {content[0]}."

    @staticmethod
    def translate_pt_to_en(content: list[str]) -> str:
        """

        """

        return f"Traduza do Português para o inglês: {content[0]}."
