import os
import pdfplumber
import requests
import re


class PDFReader:
    """
    Read a pdf file and return a processed text.
    """

    @staticmethod
    def read_pdf(file_name: str, url: str, num_pages: int = 13) -> str:
        """
        Read the pdf file.

        :param file_name: (str) with the name of the pdf file.
        :param url: (str) with the url to download the pdf file, if it was not done yet.
        :param num_pages: (int) with the last page to be read.

        :return: (str) with the content of the text.
        """

        if not os.path.exists(file_name):
            r = requests.get(url)
            with open(file_name, "wb") as f:
                f.write(r.content)

        text = ""
        with pdfplumber.open(file_name) as pdf:
            for idx in range(num_pages):
                page = pdf.pages[idx]
                text += page.extract_text() + " "

        return text

    @staticmethod
    def split_sections(text: str, include_section_title: bool = True) -> list[str]:
        """
        Split the text in sections according to the identification number (e.g., 1.1, 2.3.1, etc...)

        :param text: (str) with the text.
        :param include_section_title: (bool) indicating whether to include the main section together or not.

        :return: (list[str]) with the texts os each section.
        """

        sections = []
        # pattern for item/subitem identification
        pattern = re.compile(r'^(\d+(\.\d+)*\.?\s+.+)', re.MULTILINE)

        found_items = list(pattern.finditer(text))
        current_section = ""

        for i, item_match in enumerate(found_items):
            item = item_match.group(0).strip()
            item_number = re.match(r'^\d+(\.\d+)*', item)
            level = item_number.group(0).count('.') if item_number else 0
            if level == 0:
                current_section = item

            begin_text = item_match.end()
            if i + 1 < len(found_items):
                end_text = found_items[i + 1].start()
            else:
                end_text = len(text)

            if level > 0:
                if include_section_title:
                    section = f"{item} Texto referente a seção {current_section}: {item} {text[begin_text:end_text].strip()}"
                else:
                    section = f"{item} {text[begin_text:end_text].strip()}"
                sections.append(section)

        return sections

    @staticmethod
    def process_text(sections: list[str], max_section_length: int = 500) -> list[str]:
        """
        Perform basic cleaning of the text.

        :param sections: (list[str]) with the sections to be processed.
        :param max_section_length: (int) with the maximum length of the section.

        :return: (list[str]) with the processed text of each section.
        """

        new_sections = []
        for text in sections:
            # Remove multiple blank spaces
            clean_text = re.sub(r'\s+', ' ', text)
            # Remove spaces before punctuation
            clean_text = re.sub(r'\s+([.,;!?])', r'\1', clean_text)
            max_len = min(max_section_length, len(clean_text))
            new_sections.append(clean_text[:max_len])

        return new_sections

    def get_list_of_sections(self, file_name: str, url: str, text_config: dict = None):
        """
        Get a list with the processed sections of the text for training.

        :param file_name: (str) with the name of the pdf file.
        :param url: (str) with the url to download the pdf file, if it was not done yet.
        :param text_config: (dict) with optional configuration for extract the data.
        The possible options are: "num_pages": (int) with the last page to be read.
                                  "include_section_title": (int) with the maximum length of the section.
                                  "max_section_length": (bool) indicating whether to include the main
                                        section together or not.

        :return: (list[str]) with the processed text of each section.
        """

        if text_config is None:
            text_config = {}
        text = self.read_pdf(file_name, url, num_pages=text_config.get("num_pages", 13))
        sections = self.split_sections(text, text_config.get("include_section_title", True))
        processed_sections = self.process_text(sections, text_config.get("max_section_length", 500))

        return processed_sections
