from datetime import date, time, datetime
import yaml
import requests
import ssl
import json


class APIDataSource:
    """
    This class interacts with the government's API
    """

    def __init__(self):
        self._website = 'https://api.govinfo.gov'
        self._CONFIG_FILE = "E:\\Users\\Brad\\Documents\\billspy.config.yaml"
        self._API_key = None
        with open(self._CONFIG_FILE) as f:
            configuration = yaml.safe_load(f)
            self._API_key = configuration['API_key']

    def get_bills_listing(self, start_date: date, end_date: date):
        iso_midnight_str = 'T00:00:00Z'  # might need to replace : with %3A
        #start = start_date.isoformat()
        #start = start.join(iso_midnight_str)
        #end = end_date.isoformat().join(iso_midnight_str)
        midnight = time(0, 0, 0)
        start = datetime.combine(start_date, midnight).isoformat()
        end = datetime.combine(end_date, midnight).isoformat()

        collection = 'BILLS'
        page_size = 100
        offset = 0
        all_bills = []

        while True:

            url = f'{self._website}/collections/{collection}/{start}Z/{end}Z?offset={offset}&pageSize={page_size}'
            # print(url)
            self._append_api_key(url)
            result = self._execute_query(url)
            data = json.loads(result)
            print(data.keys())
            # print(data['validationMessages'])
            packages = data['packages']
            all_bills.extend(packages)

            if data['nextPage'] is None:
                break

            offset = offset + page_size

        return all_bills


    def _append_api_key(self, url):
        new_url = url
        if '?' not in new_url:
            #new_url = ''.join(new_url, '?')
            new_url += '?'
        new_url = new_url + f'&api_key={self._API_key}'
        return new_url
        # return new_url(f'&api_key={self._API_key}')

    def _execute_query(self, url: str) -> str:
        url = self._append_api_key(url)
        print(url)
        # response = urllib.request.urlopen(url)
        # data = response.read()
        # text = data.decode('utf8', 'ignore')

        # This line is for testing purposes -- To be deleted when I've got things working
        # url = 'https://api.govinfo.gov/collections?api_key=AlGT2EfGtbvovEqIWBjQC2ubL8Xj3rsdSBduXISa'

        response = requests.get(url)
        print(response.content)
        return response.text

        #
        # headers = {
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        #     "Accept-Encoding": "gzip, deflate",
        #     "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        #     "Dnt": "1",
        #     "Host": "httpbin.org",
        #     "Upgrade-Insecure-Requests": "1",
        #     # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        #     # 'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; rv:2.2) Gecko/20110201'
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'
        # }
        #
        # data = ''
        # try:
        #     # Gives 404 Not Found error if including headers.  Otherwise, gives a 400 Bad Request Error
        #     request = urllib.request.Request(url, data=None, headers=headers)
        #
        #     # to ignore ssl certificate errors.  Gives a 404 Not Found error
        #     ctx = ssl.create_default_context()
        #     ctx.check_hostname = False
        #     ctx.verify_mode = ssl.CERT_NONE
        #     html = urllib.request.urlopen(request, context=ctx).read()
        #
        #     response = urllib.request.urlopen(request)
        #     page = response.read()
        #     data = page.decode('utf8', 'ignore')
        # except urllib.error.HTTPError as e:
        #     print(e)
        # return data
