class Prompts:
    """

    """

    def prompt_factory(self, option: str):
        """

        :param option:
        :return:
        """

        if option == "correct_en":
            return self.correct_answer_en
        elif option == "wrong_en":
            return self.wrong_answer_en
        elif option == "make_question_en":
            return self.make_question_en
        elif option == "summarize_en":
            return self.summarize_en
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

        return f"""
        Answer the following question based on the text. Avoid single-word answer.
        Text: {content[1]}
        Question: {content[0]}"""

    @staticmethod
    def wrong_answer_en(content: list[str]) -> str:
        """

        """

        return f"""Generate a plausible but incorrect answers for the following
        question. Please, do not repeat the correct answer.
        Question: {content[0]}
        Correct answer: {content[1]}
        Context: {content[2]}"""

    @staticmethod
    def make_question_en(content: list[str]) -> str:
        """

        """

        prompt = f"""Generate a clear and concise question from the text.
        The question should be factual and directly answerable from the text.
        Text: {content[0]}
        Question:"""

        return prompt

    @staticmethod
    def summarize_en(content: list[str]) -> str:
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
