from datetime import date, time, datetime
from Models.configData import ConfigData
import json
from bs4 import BeautifulSoup

import yaml
import requests
import ssl
import json
import urllib


class APIDataSource:
    """
    This class interacts with the government's API
    """
    _website = 'https://api.govinfo.gov'
    _API_key = ConfigData.get_config_dict()['API_key']
    _does_not_exist_message = 'The requested resource does not exist.'

    @classmethod
    def store(cls, bill_id, text, is_metadata=False):
        raise NotImplementedError("API can't store data")

    @classmethod
    def get(cls, bill_id, is_metadata=False):
        # get the package link
        # get the bill text link from the dict
        package = json.loads(cls._get_package_data(bill_id))
        if is_metadata:
            return package
        else:
            url = package['download']['txtLink']
            html = cls._execute_query(url)
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.text
            return text

    @classmethod
    def does_bill_exist(cls, bill_id, is_metadata=False):
        package = cls._get_package_data(bill_id)
        is_there_a_message = 'message' in package
        return not (is_there_a_message and cls._does_not_exist_message in package['message'])

    @classmethod
    def yield_bill_ids(cls, star_date, end_date):
        packages = cls._get_list_of_packages(star_date, end_date)
        for package in packages:
            yield package['packageId']

    @classmethod
    def _get_dict_from_link(cls, url):
        data = cls._execute_query(url)
        dictionary = json.loads(data)
        return dictionary

    @classmethod
    def _get_package_data(cls, bill_id):
        url = f'{cls._website}/packages/{bill_id}/summary'
        package = cls._execute_query(url)
        return package

    @classmethod
    def _get_list_of_packages(cls, start_date: date, end_date: date):
        start = start_date.isoformat()
        end = end_date.isoformat()
        page_size = 100
        collection = 'BILLS'
        offset_mark = '*'
        url = f'{cls._website}/published/{start}/{end}?pageSize={page_size}&collection={collection}&offsetMark={offset_mark}'

        error_msgs = {'Error encountered while processing this request .',
                      'No results found'}

        all_packages = []

        while True:
            result = cls._execute_query(url)
            data = json.loads(result)

            message = data['message']

            # stop if there is an error message
            if message in error_msgs:
                break

            # stop if there are no packages or packages is empty
            if 'packages' not in data.keys() or len(data['packages']) == 0:
                break

            # add the new data to all_packages
            packages = data['packages']
            all_packages.extend(packages)

            # if there is no next page, stop
            next_page = data['nextPage']
            if not next_page:
                break
            url = next_page

        return all_packages

    def _get_bill_text(self, bill_id):
        url = f'{self._website}/packages/{bill_id}/htm'
        url = self._append_api_key(url)
        return self._execute_query(url)

    def _get_bill_pdf(self, bill_id):
        url = f'https://www.govinfo.gov/content/pkg/{bill_id}/pdf/{bill_id}.pdf'
        return self._execute_query(url)

    @classmethod
    def _append_api_key(cls, url):
        new_url = url
        if '?' not in new_url:
            #new_url = ''.join(new_url, '?')
            new_url += '?'
        new_url = new_url + f'&api_key={cls._API_key}'
        return new_url
        # return new_url(f'&api_key={self._API_key}')

    @classmethod
    def _execute_query(cls, url: str) -> str:
        url = cls._append_api_key(url)
        # print(url)
        response = requests.get(url)
        return response.text

