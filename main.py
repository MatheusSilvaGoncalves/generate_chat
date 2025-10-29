from transformers import logging
import random
from typing import Callable
from file_reader import PDFReader
from models.pt_en_question_generator import PtEnQuestionGenerator
from models.question import Question


logging.set_verbosity_error()


def question_handling(cont: int, question: Question):
    """

    :return:
    """

    print(f"\nPergunta {cont}: {question.question}")
    for i, alt in enumerate(question.alternatives):
        print(f"{i + 1}) {alt[1]}")

def answer_handling(question: Question, evaluate: Callable):
    """

    :return:
    """

    selected = input("Escolha a alternativa correta (1-4): ")
    try:
        selected_int = int(selected) - 1
        if not -1 < selected_int < 4:
            raise ValueError
        response, value = evaluate(question, selected_int)
        print(response)

        return value
    except:
        print("Entrada inválida. Digite um número entre 1 e 4.")


def iniciar_chat():
    print("=== Concurso Renda Extra Ton ===")
    url = "https://documentos.ton.com.br/rendaextra-todos-regulamentos.pdf"
    file_name = "regulamento.pdf"
    n_questions = 10
    points = 0
    pdf_reader = PDFReader()
    total_text = pdf_reader.get_list_of_sections(file_name, url)
    generator = PtEnQuestionGenerator("Batata")
    for idx in range(n_questions):
        selected_text = random.choice(total_text)
        print(selected_text)
        total_text.remove(selected_text)
        question = generator.generate(selected_text, n_alternatives=4)
        question_handling(idx + 1, question)
        points += answer_handling(question, generator.evaluate_answer)

    print(f"Teste finalizado! Sua pontuação foi {points}/{n_questions}")


if __name__ == "__main__":
    random.seed(0)
    iniciar_chat()
