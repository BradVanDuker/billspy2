from Models.dataSource import DataSource
from collections import namedtuple
from datetime import date
from Control.trainingControler import TrainingController

class CLI_Interface:
    def __init__(self):
        self.datasource = DataSource()

    def run(self):
        self._main_menu()

    def exit_program(self):
        exit()

    def _main_menu(self):
        MenuOption = namedtuple('MenuOption', ['text', 'call'])
        options = [MenuOption('Corpus Cache', self._download_corpus_cache_menu),
                   MenuOption('Train Model', self._train_menu),
                   MenuOption('Classify Bill', self._classify_bill_menu),
                   MenuOption('View Cluster Keywords', self._view_clusters_menu),
                   MenuOption('Exit', self.exit_program)]

        selected_option = None
        enumerated_options = list(enumerate(options))

        while True:
            for i, option in enumerated_options:
                print(f'{i}:  {option.text}')
            user_input = input('Select option number:  ')

            user_selection = [(i, menu_option) for i, menu_option in enumerated_options if str(i) == user_input]
            if len(user_selection) == 1:
                foo, selected_option = user_selection[0]
                break
            else:
                print('Invalid selection')

        selected_option.call()

    @staticmethod
    def _get_dates_from_user():
        while True:
            while True:
                start_date_input = input('Enter starting date in YYYY-MM-DD format:  ')
                try:
                    start_date = date.fromisoformat(start_date_input)
                    break
                except ValueError:
                    print('Invalid Starting Date')

            while True:
                end_date_input = input('Enter ending date in YYYY-MM-DD format:  ')
                try:
                    end_date = date.fromisoformat(end_date_input)
                    break
                except ValueError:
                    print('Invalid Ending Date')

            if start_date >= end_date:
                print('Starting date must be before ending date.')
                continue
            else:
                break

        return start_date, end_date

    def _download_corpus_cache_menu(self):
        start_date, end_date = self._get_dates_from_user()

        bill_id_gen = self.datasource.yield_list_of_bill_ids(start_date, end_date)

        for bill_id in bill_id_gen:
            self.datasource.cache_bill(bill_id)

    def _train_menu(self):
        # get date range of training data (bills) from user
        start_date, end_date = self._get_dates_from_user()

        # get number of clusters
        while True:
            num_of_clusters_response = input('Enter number of clusters:  ')
            try:
                num_of_clusters = int(num_of_clusters_response)
                break
            except ValueError as e:
                print('Please enter a valid integer')

        # get bill numbers
        bill_ids = list(self.datasource.yield_list_of_bill_ids(start_date, end_date))

        tc = TrainingController(self.datasource)
        print('processing...')
        tc.run(bill_ids, num_of_clusters)



        pass

    def _view_clusters_menu(self):
        pass

    def _classify_bill_menu(self):
        pass
