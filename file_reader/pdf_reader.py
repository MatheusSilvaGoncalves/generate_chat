import os
import pdfplumber
import requests
import re


class PDFReader:
    """
    Read a pdf file and return a processed text.
    """

    def read_pdf(self, file_name: str, url: str, num_pages: int = 13) -> str:
        """
        Read the pdf file.

        :param file_name: (str) with the name of the pdf file.
        :param url: (str) with the url to download the pdf file, if it was not done yet.
        :param num_pages: (int) with the last page to be read.
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
    def split_sections(text):
        """
        Divide o texto em seções com base em títulos numerados.
        Retorna uma lista de dicionários: {"titulo": ..., "texto": ...}
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
                section = f"Texto referente a seção {current_section}: {item} {text[begin_text:end_text].strip()}"
                sections.append(section)

        return sections

    @staticmethod
    def process_text(sections: list[str]) -> list[str]:
        """
        Perform basic cleaning of the text.
        """

        new_sections = []
        for text in sections:
            # Remove multiple blank spaces
            clean_text = re.sub(r'\s+', ' ', text)
            # Remove spaces before punctuation
            clean_text = re.sub(r'\s+([.,;!?])', r'\1', clean_text)
            new_sections.append(clean_text)

        return new_sections

    @staticmethod
    def group_by_main_content(sections):
        """
        Group items according to a same content (e.g., section 1.1 and 1.2)
        """

        grouped = []
        current_section = None

        for s in sections:
            if s["level"] == 0:
                if current_section:
                    grouped.append(current_section)
                current_section = {
                    "item": s["item"],
                    "text": s["text"],
                    "subitems": []
                }
            elif s["level"] == 1 and current_section:
                current_section["subitems"].append(s)
            elif s["level"] > 1 and current_section and current_section["subitems"]:
                current_section["subitems"][-1]["text"] += "\n" + s["text"]

        if current_section:
            grouped.append(current_section)

        return grouped

    def generate_training_block(self, sections: list[dict], mode="grouped"):
        """
        Create blocks of text for training.

        mode = 'single' independent sections.
        mode = 'grouped' group together items according to main section content.
        """

        blocks = []
        if mode == "single":
            current_title = ""
            for s in sections:
                if s['level'] > 0:
                    blocks.append({
                        "context": current_title,
                        "text": s["item"] + s["text"],
                    })
                else:
                    current_title = s["item"]
        elif mode == "grouped":
            grouped = self.group_by_main_content(sections)
            for g in grouped:
                whole_text = g["text"]
                for sub in g["subitems"]:
                    whole_text += f"\n{sub['item']}\n{sub['text']}"
                blocks.append({
                    "context": g["item"],
                    "text": whole_text,
                })
        return blocks

    def get_list_of_sections(self, file_name: str, url: str, num_pages: int = 13,
                             mode: str = 'single'):
        """
        Get a list of sections of the text.

        :param file_name: (str) with the name of the pdf file.
        :param url: (str) with the url to download the pdf file, if it was not done yet.
        :param num_pages: (int) with the last page to be read.
        """

        text = self.read_pdf(file_name, url, num_pages=num_pages)
        sections = self.split_sections(text)
        processed_sections = self.process_text(sections)

        return processed_sections
