import re

class HTMLParser:
    @staticmethod
    def _lop_off_top(text: str):
        starting_str = 'SECTION 1.'
        starting_pos = text.find(starting_str) + len(starting_str)
        return text[starting_pos:]

    @staticmethod
    def _lop_off_botton(text):
        ending_pos = text.find('____')
        return text[:ending_pos]

    @staticmethod
    def _lop_off_ends_of_lines(section_of_text):
        line = section_of_text.replace('\n', ' ')
        line = line.strip()
        return line

    @staticmethod
    def _break_into_sections(text) -> [str]:
        regx_str = 'SEC\.'
        rx = re.compile(regx_str)
        matches = [i for i in rx.finditer(text)]
        parts = []
        end = len(text)
        for i in range(len(matches) - 1):
            start = matches[i].start()
            end = matches[i + 1].start()
            parts.append(text[start:end])
        parts.append(text[end:])
        return parts

    @staticmethod
    def _reduce_chunk_to_line(chunk: str):
        string = chunk.strip().replace('\n', '')


    @staticmethod
    def _break_section_into_paragraphs(section):
        x = r'(    )*(\([a-zA-Z0-9]\))'
        string = section.strip().replace('\n', '')
        strings = string.split(' ')
        words = [w.strip() for w in strings if w != '']
        return_line = ''
        for w in words:
            return_line += w + ' '
        return_paragraphs.append(return_line)
        return return_paragraphs

    @staticmethod
    def parse_text(text):
        text = HTMLParser._lop_off_top()
        text = HTMLParser._lop_off_botton()
        sections = HTMLParser._break_into_sections()
        paragraphs = []
        for section in sections:
            paragraphs.extend()