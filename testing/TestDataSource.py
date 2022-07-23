import unittest
import os

from Models.dataSource import DataSource
from Models.configData import ConfigData


class TestDataSource(unittest.TestCase):
    corpus_directory = ConfigData.get_config_dict()['corpus_directory']

    def test_get_bill_text_if_exists(self):
        # first write the file so it exists
        doc_name = 'foobar.txt'
        answer_text = 'This is sample text.'
        is_metadata = False
        filepath = os.path.join(self.corpus_directory, 'raw')
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        full_file_name = os.path.join(filepath, doc_name)
        with open(full_file_name, mode='w+') as f:
            f.write(answer_text)

        # test if the text returned matches the text written
        ds = DataSource()
        response_text = ds.get('foobar.txt')
        self.assertEqual(response_text, answer_text, 'response and answer texts do not match')

        # remove the file
        os.remove(full_file_name)

    def test_get_bill_text_if_not_exists(self):
        bill_id = 'BILLS-117hr7733rh'

        # ensure bill does not exist locally
        full_file_name = os.path.join(self.corpus_directory, 'raw', bill_id)
        was_file_present = os.path.exists(full_file_name)
        text_copy = ''
        if was_file_present:
            with open(full_file_name) as f:
                text_copy = f.read()
            os.remove(full_file_name)

        # get the text
        ds = DataSource()
        response_text = ds.get(bill_id)

        # check the response is correct
        answer_fragment = 'To amend the Community Development Banking and Financial Institutions'
        self.assertTrue(answer_fragment in response_text)

        # restore the file to its original state
        if was_file_present:
            with open(full_file_name, mode='w+') as f:
                f.write(text_copy)


if __name__ == '__main__':
    unittest.main()