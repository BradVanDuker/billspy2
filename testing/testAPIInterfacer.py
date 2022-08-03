import unittest
from Models.apiDataSource import APIDataSource


class TestAPIInterfacer(unittest.TestCase):
    def test__append_api_key(self):
        interfacer = APIDataSource()
        url = ''
        url = interfacer._append_api_key(url)
        answer = ''.join(f'?&api_key={interfacer._API_key}')
        self.assertEqual(answer, url)

    def test__execute_url(self):
        interfacer = APIDataSource()
        url = 'https://api.govinfo.gov/collections'
        response = interfacer._execute_query(url)
        self.assertTrue('collectionName' in response)

    def test_get_bill_text(self):
        data_source = APIDataSource()
        bill_id = 'BILLS-117hr7733rh'
        text = data_source.get_bill_text(bill_id)
        paragraph = 'To amend the Community Development Banking and Financial Institutions'
        # self.assertIn(paragraph, text, "paragraph not in the text")
        self.assertTrue(paragraph in text, 'paragraph not in the text')


if __name__ == '__main__':
    unittest.main()
