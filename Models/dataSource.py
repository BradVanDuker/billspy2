from os import path

from Models.apiDataSource import APIDataSource
from Models.fileDataSource import FileDataSource


class DataSource:
    def __init__(self):
        self.api_data_source = APIDataSource()
        self.file_data_source = FileDataSource()

    def yield_list_of_bill_ids(self, start_date, end_date):
        return self.api_data_source.yield_bill_ids(start_date, end_date)

    def get(self, bill_id: str, to_cache=False) -> str | None:
        # First try to get the text from file.  If it doesn't exist, try the gov's api
        if self.file_data_source.does_bill_exist(bill_id):
            print(f'reading {bill_id} from file')
            return self.file_data_source.get(bill_id)
        else:
            text = self.api_data_source.get(bill_id)
            print(f'downloading {bill_id} from api')
            if to_cache:  # if we're caching, write it to file
                print(f'writing {bill_id} to cache')
                self.file_data_source.store(bill_id, text)
            return text

    def store(self, bill_id, text: str, is_metadata=False):
        self.file_data_source.store(bill_id, text, is_metadata)

    def get_cached_bill_list(self, is_metadata=False):
        return self.file_data_source.get_bill_ids(is_metadata=is_metadata)

    def cache_bill(self, bill_id: [str]):
        if not self.file_data_source.does_bill_exist(bill_id):
            text = self.api_data_source.get(bill_id)
            self.file_data_source.store(bill_id, text)
