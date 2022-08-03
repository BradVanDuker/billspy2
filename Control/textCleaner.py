import re

class TextCleaner:

    @classmethod
    def get_bill_text(cls, bill_raw):
        top_sentinel = 'A BILL'
        return cls._get_just_main_text(top_sentinel, bill_raw)

    @classmethod
    def get_resolution_text(cls, resolution_raw):
        top_word = 'RESOLUTION'
        return cls._get_just_main_text(top_word, resolution_raw)

    @classmethod
    def get_act_text(cls, act_raw: str):
        top_sentinel = 'AN ACT'
        return cls._get_just_main_text(top_sentinel, act_raw)

    @classmethod
    def _get_just_main_text(cls, top_word, text):
        starting_index = text.lower().find(top_word.lower()) + len(top_word)
        return_text = text[starting_index:]

        patterns = {r'\s+\<all\>', r'\n\s+Calendar No\.',
                    r'\n\n\s+(Passed the House of Representatives)|(Passed the Senate)',}
        for p in patterns:
            match = re.search(p, return_text)
            if match:
                # print(f'Found {match[0]}')
                ending_index = match.start()
                return return_text[:ending_index]
        else:
            return_text = text[starting_index:]
            return_text = cls._remove_big_lines(return_text)
            # return_text = cls._remove_big_lines(return_text)
            return return_text



    @staticmethod
    def _remove_big_lines(text):
        x = r'\n_+\n'
        match = re.search(x, text)
        while match:
            line = text[match.start():match.end()]
            text = text.replace(line, ' ')
            match = re.search(x, text)
        return text
