from transformers import logging
import random
from typing import Callable
from file_reader import PDFReader
from models import QuestionGenerator
from models import Question


logging.set_verbosity_error()


def question_handling(cont: int, question: Question):
    """
    Method to perform the question to the user.

    :param cont: (int) with the question's number.
    :param question: (Question) with the multiple choice question object.
    """

    print(f"\nPergunta {cont}, referente ao item {question.question}")
    for i, alt in enumerate(question.alternatives):
        print(f"{i + 1}) {alt[1]}")

def answer_handling(question: Question, evaluate: Callable):
    """
    Method to get user's answer to a given question.

    :param question: (Question) with the multiple choice question object.
    :param evaluate: (Callable) with the method to evaluate the answer.
    """

    while True:
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


def start_chat(title: str, n_questions: int, model_config: dict, text_config: dict = None, debug: bool = False,
               pt_en_pt: bool = True, n_alternatives: int = 4, max_tries: int = 5):
    """
    Method that performs the complete quiz workflow.

    :param title: (str) with the title of the quiz.
    :param n_questions: (int) with the number of questions.
    :param model_config: (dict) with the configuration of the workflow.
    :param text_config: (dict) with optional configuration for extract the data.
    :param debug: (bool) indicating whether to show the intermediate steps or not.
    :param pt_en_pt: (bool) indicating whether to translate the workflow for english or not.
    :param n_alternatives: (int) with the number of alternatives to be created.
    :param max_tries: (int) with maximum number of tries for generating different alternatives.
    """

    print(title)
    url = "https://documentos.ton.com.br/rendaextra-todos-regulamentos.pdf"
    file_name = "regulamento.pdf"
    points = 0
    pdf_reader = PDFReader()
    total_text = pdf_reader.get_list_of_sections(file_name, url, text_config)
    generator = QuestionGenerator(model_config, total_text, pt_en_pt)
    for idx in range(n_questions):
        question = generator.generate(n_alternatives=n_alternatives, debug=debug, max_tries=max_tries)
        question_handling(idx + 1, question)
        points += answer_handling(question, generator.evaluate_answer)

    print(f"Teste finalizado! Sua pontuação foi {points}/{n_questions}")


if __name__ == "__main__":
    # Example of model's use

    random.seed(0)
    model_config_dict = {"processing":
                             [{"task": "summarization",
                               "name": "sshleifer/distilbart-cnn-12-6"}],
                         "question":
                             [{"task": "text2text-generation",
                               "name": "google/flan-t5-large",
                               "prompt": "Generate a clear question based on the following text."}],
                         "correct_answer":
                             [{"task": "text2text-generation",
                               "name": "google/flan-t5-large",
                               "prompt": "Based on the text below, provide a concise, factually correct answer to the question. Do not invent information. The answer should be in one or two sentences."}],
                         "wrong_answer":
                             [{"task": "text2text-generation",
                               "name": "google/flan-t5-large",
                               "prompt": "Based on the text below, provide a concise answer to the question. The answer should be in one or two sentences.",
                               "distractor": True,
                               "kwargs":
                                   {"max_new_tokens": 100,
                                    "temperature": 0.8}},
                              {"task": "text2text-generation",
                               "name": "google/flan-t5-large",
                               "prompt": "Based on the text below, provide a concise answer to the question. The answer should be in one or two sentences.",
                               "distractor": True,
                               "kwargs":
                                   {"max_new_tokens": 100,
                                    "temperature": 0.5}},
                              {"task": "text2text-generation",
                               "name": "google/flan-t5-large",
                               "prompt": "Based on the text below, provide a concise answer to the question. The answer should be in one or two sentences.",
                               "distractor": True,
                               "kwargs":
                                   {"max_new_tokens": 100,
                                    "temperature": 0.9}}
                              ]
                         }
    text_config_dict = {'max_section_length': 500, 'include_section_title': False}
    view_debug = True
    translate = True
    new_title = "=== Concurso Renda Extra Ton ==="
    start_chat(new_title, 10, model_config_dict, text_config_dict, view_debug, translate, 4)
