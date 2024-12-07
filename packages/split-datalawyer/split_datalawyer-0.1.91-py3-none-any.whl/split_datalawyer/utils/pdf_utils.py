# #!/usr/bin/env python
# # coding: utf-8

import fitz
import re
import html

from typing import List, Union
from pathlib import Path

from split_datalawyer.utils.regex_utils import __SPLIT_SPACES__, re_tree_dots, re_dotted_line, re_changehyphen, \
    re_quotes_1, re_quotes_2, re_quotes_3, re_dots, re_punctuation, re_doublequotes_1, re_doublequotes_2, re_trim, \
    item_replacement, re_page_numbers, pattern_punctuation, __CNJ_NUMBER__, section_number_exceptions, \
    __REGEX_SECTION_NUMBERS__, __ELLIPSIS__

final_punctuations = '.;:")?!'


def merge_split_words(content: str) -> str:
    return __SPLIT_SPACES__.sub(r"\1", content)


def clean_text(text):
    """Apply all regex above to a given string."""
    text = html.unescape(text)
    text = text.replace('\xa0', ' ')
    text = re_tree_dots.sub('...', text)
    text = re_dotted_line.sub('.....', text)
    text = re_changehyphen.sub(item_replacement, text)
    text = re_quotes_1.sub(r'\1"', text)
    text = re_quotes_2.sub(r'"\1', text)
    text = re_quotes_3.sub('"', text)
    text = re_dots.sub('.', text)
    text = re_punctuation.sub(r'\1', text)
    text = re_doublequotes_1.sub('\"', text)
    text = re_doublequotes_2.sub('\'', text)
    text = re_trim.sub(' ', text)
    text = replace_chars_in_interval(text, 61000, 128000, item_replacement)
    text = replace_chars_in_interval(text, 127, 159, '')
    text = re.sub(r'\s+', ' ', text)
    text = re_page_numbers.sub('', text)
    return text.strip()


def is_upper(text: str, strip_non_alpha: bool = True) -> bool:
    if strip_non_alpha:
        return re.sub('[^A-Za-z0-9]+', '', text).isupper()
    else:
        return text.isupper()


def starts_with_upper(text: str) -> bool:
    return len(text.strip()) > 0 and is_upper(text[0])


def strip_punctuation(word: str) -> str:
    return re.sub(pattern_punctuation, ' ', word)


def match(text: str, regex: re.Pattern):
    return len(regex.findall(text)) > 0


def ends_with_punctuation(text: str) -> bool:
    return len(text.strip()) > 0 and match(text=text[-1], regex=pattern_punctuation)


def is_cnj_number(text: str) -> bool:
    return match(text=text, regex=__CNJ_NUMBER__)


def is_section_number(text: str) -> bool:
    return text.lower() not in section_number_exceptions and not is_cnj_number(text) and \
        not text.lower().startswith('e-mail') and any(regex.match(text) for regex in __REGEX_SECTION_NUMBERS__)


def starts_with_section_number(text: str) -> bool:
    return len(text.strip()) > 0 and is_section_number(text.split()[0])


def starts_with_ellipsis(text: str) -> bool:
    return match(text, __ELLIPSIS__)


keep_codes = [8, 9, 10, 13, 730, 8208, 8209, 8210, 8211, 8212, 8213, 8214, 8216, 8217, 8218, 8219, 8220, 8221, 8222,
              8223, 8226, 8230]


def clean_non_ascii_characters(text: str) -> str:
    return ''.join([i if (31 < ord(i) < 256 or ord(i) in keep_codes) else '' for i in text]).strip()


def replace_chars_in_interval(text, start, end, replacement):
    result = []
    for char in text:
        char_code = ord(char)
        if start <= char_code <= end:
            result.append(replacement)
        else:
            result.append(char)
    return ''.join(result)


def extract_pdf_text(pdf_path: Union[str, Path]) -> str:
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text += page.get_text(sort=True)
    return text


def split_pdf_lines(text: str) -> List[str]:
    return re.sub(r"^\d{1,2}(\s?)$", r'\n', text, 0, re.MULTILINE).splitlines()


def load_pdf_lines_from_path(pdf_path: Union[str, Path]) -> List[str]:
    return split_pdf_lines(extract_pdf_text(pdf_path))


def merge_split_sections(paragraphs: List[str]) -> List[str]:
    # Merge paragraphs that appear to be section numbers with the following sentence
    merged = []
    i = 0
    while i < len(paragraphs):
        if is_section_number(paragraphs[i]):
            if (i + 1) < len(paragraphs):
                if not is_section_number(paragraphs[i + 1]) and not paragraphs[i + 1].startswith(item_replacement):
                    merged.append(paragraphs[i] + ' ' + paragraphs[i + 1])
                    i += 2
                else:
                    merged.append(paragraphs[i])
                    i += 1
            else:
                merged.append(paragraphs[i])
                i += 1
        else:
            merged.append(paragraphs[i])
            i += 1

    return merged


def debug_line_count(pdf_path: Union[str, Path], print_page_number: int = None):
    pdf_document = fitz.open(pdf_path)
    lines_lengths = []
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        if print_page_number and page_number == print_page_number:
            for line in page.get_text().splitlines():
                print(line)
        lines_lengths.append(len(page.get_text().splitlines()))
        print(f'Page {page_number}: {len(page.get_text().splitlines())} lines and {len(page.get_text_blocks())} blocks')
    print(sum(lines_lengths) / len(lines_lengths))
