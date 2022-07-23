import re

from Models.dataSource import DataSource


class TrainingController:
    def __init__(self, datasource: DataSource):
        self.datasource = datasource

    def train_model(self, list_of_bill_ids):
        # get the data
        for bill_id in list_of_bill_ids:
            text = self.datasource.get(bill_id)
            pass
        # clean up the data
        # save the cleaned up data to the proper location
        # use the clean data for training

    @staticmethod
    def _lop_off_top(text: str):
        starting_str = 'SECTION 1.'
        starting_pos = text.find(starting_str) + len(starting_str)
        return text[starting_pos:]

    @staticmethod
    def _lop_off_bottom(text):
        ending_pos = text.find('____')
        return text[:ending_pos]







