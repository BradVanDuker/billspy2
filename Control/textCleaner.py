import re

class TextCleaner:
    @staticmethod
    def _cut_off_top(text: str):
        starting_str = 'SECTION 1.'
        starting_pos = text.find(starting_str) + len(starting_str)
        return text[starting_pos:]

    @staticmethod
    def _cut_off_bottom(text):
        ending_pos = text.find('____')
        return text[:ending_pos]



    @classmethod
    def get_cleaned_text(cls, text):
        headless_text = cls._cut_off_top(text)
        trunc_text = cls._cut_off_bottom(headless_text)
        return trunc_text

    @staticmethod
    def get_resolution_text(resolution_text):
        raise NotImplementedError()

