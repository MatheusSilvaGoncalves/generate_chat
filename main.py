from transformers import logging
import random
from typing import Callable
from file_reader import PDFReader
from models.question_generator import QuestionGenerator
from models.question import Question


logging.set_verbosity_error()


def question_handling(cont: int, question: Question):
    """

    :return:
    """

    print(f"\nPergunta {cont}, referente ao item {question.question}")
    for i, alt in enumerate(question.alternatives):
        print(f"{i + 1}) {alt[1]}")

def answer_handling(question: Question, evaluate: Callable):
    """

    :return:
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


def start_chat(n_questions: int, model_config: dict, text_config: dict = None, debug: bool = False,
               pt_en_pt: bool = True, n_alternatives: int = 4):
    print("=== Concurso Renda Extra Ton ===")
    url = "https://documentos.ton.com.br/rendaextra-todos-regulamentos.pdf"
    file_name = "regulamento.pdf"
    points = 0
    pdf_reader = PDFReader()
    total_text = pdf_reader.get_list_of_sections(file_name, url, text_config)
    generator = QuestionGenerator(model_config, total_text, pt_en_pt)
    for idx in range(n_questions):
        question = generator.generate(n_alternatives=n_alternatives, debug=debug)
        question_handling(idx + 1, question)
        points += answer_handling(question, generator.evaluate_answer)

    print(f"Teste finalizado! Sua pontuação foi {points}/{n_questions}")


if __name__ == "__main__":
    random.seed(0)
    model_config_dict = {"processing":
                             [{"task": "summarization",
                               "name": "sshleifer/distilbart-cnn-12-6"}],
                         "question":
                             [{"task": "text2text-generation",
                               "name": "google/flan-t5-base",
                               "prompt": "Generate a clear and concise question from the text. The question should be factual and directly answerable from the text."}],
                         "correct_answer":
                             [{"task": "text2text-generation",
                               "name": "google/flan-t5-base",
                               "prompt":
                                   "Answer the following question based on the text. Avoid single-word answers."}],
                         "wrong_answer":
                             [{"task": "text2text-generation",
                               "name": "google/flan-t5-base",
                               "prompt": "Generate a plausible but incorrect answer for the following question. Please, do not repeat the correct answer.",
                               "distractor": True,
                               "kwargs":
                                   {"max_new_tokens": 100,
                                    "temperature": 1,
                                    "top_k": 50}},
                              {"task": "text2text-generation",
                               "name": "google/flan-t5-base",
                               "prompt": "Generate a clearly incorrect answer for the following question. Please, do not repeat the correct answer.",
                               "kwargs":
                                   {"max_new_tokens": 25,
                                    "temperature": 1.5,
                                    "top_k": 5}},
                              {"task": "text2text-generation",
                               "name": "google/flan-t5-base",
                               "prompt": "Modify the correct answer to be false. Please, do not repeat the correct answer.",
                               "kwargs":
                                   {"max_new_tokens": 200,
                                    "temperature": 0.5,
                                    "top_k": 10}}
                              ]
                         }
    text_config_dict = {'max_section_length': 500, 'include_section_title': False}
    view_debug = True
    pt_en_pt = True
    start_chat(10, model_config_dict, text_config_dict, view_debug, pt_en_pt, 4)
