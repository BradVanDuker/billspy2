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


if __name__ == '__main__':
    unittest.main()
