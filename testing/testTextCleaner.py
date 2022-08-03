import unittest
import os
from Control.textCleaner import TextCleaner
from collections import namedtuple

class TestTextCleaner(unittest.TestCase):
    Test = namedtuple('Test', ['bill_id', 'included_text', 'excluded_text'])

    @staticmethod
    def _get_legislation(bill_id):
        my_path = r'E:\Users\Brad\Documents\Corpus\raw'
        with open(os.path.join(my_path, bill_id)) as f:
            text = f.read()
        return text

    def test_get_resolution_text(self):
        resolution_id = 'BILLS-117hres1156ih'
        text = self._get_legislation(resolution_id)
        cleaned_text = TextCleaner.get_resolution_text(text)

        self.assertIn('Whereas', cleaned_text)
        self.assertNotIn('117th CONGRESS', cleaned_text)

    def test_get_bill_text(self):
        tests = [self.Test('BILLS-117s4264is', 'the requirements under this subsection are the following:',
                           '117th CONGRESS'),
                 self.Test('BILLS-117S4136rs', 'the Okatibbee Lake portion of the project for flood protection',
                           '117th CONGRESS'),
                 self.Test('BILLS-117s4132pcs', 'to any person, entity, government, or circumstance, is held to be',
                           '117th CONGRESS')]

        for bill_id, included_text, excluded_text in tests:
            text = self._get_legislation(bill_id)
            cleaned_text = TextCleaner.get_bill_text(text)

            self.assertIn(included_text, cleaned_text, f'Included text not found in {bill_id}')
            self.assertNotIn(excluded_text, cleaned_text, f'Excluded text found in {bill_id}')

    def test_get_act_text(self):

        tests = [self.Test('BILLS-117hr2773eh', 'To amend the Pittman-Robertson Wildlife Restoration Act to make',
                           '117th CONGRESS'),
                 self.Test('BILLS-117hr3182enr', 'manufacture, shall be considered a banned hazardous product under',
                           '[H.R. 3182 Enrolled Bill (ENR)]'),
                 self.Test('BILLS-107hr2217rs', 'Agencies Appropriations Act, 1999, as included in Public Law 105-277,',
                           'Calendar No. 78'),
                 self.Test('Bills-107hr2217rs', "Related Agencies Appropriations Act, 2002''.", 'Calendar No. 78')]

        for act_id, included_text, excluded_text in tests:
            text = self._get_legislation(act_id)
            cleaned_text = TextCleaner.get_act_text(text)

            self.assertIn(included_text, cleaned_text, f'Included text not found in {act_id}')
            self.assertNotIn(excluded_text, cleaned_text, f'Excluded text found in {act_id}')

            pass