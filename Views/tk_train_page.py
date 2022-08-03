from datetime import date, time, datetime
import tkinter as tk
from tkinter import messagebox

from Models.dataSource import DataSource
from Control.trainingControler import TrainingController



class TrainPage(tk.Frame):
    def __init__(self, master: tk.Tk):
        super().__init__(master)

        self.datasource = DataSource()

        self.title_label = tk.Label(self, text='Training', justify='center')
        self.title_label.grid(row=0, column=0, columnspan=3)

        description_text = "Training teaches the AI model which parts of a document are important and which parts " \
                           "aren't.  You should only have to train once.  The more text you train on the better the " \
                           "summaries will be.  The process will take up a large amount of diskspace and time.  " \
                           "Once the training is done you can safely delete the files it used.  Specify the location " \
                           "to which data will be saved using the config file."
        self.description_label = tk.Label(self, text=description_text, wraplength=800, justify='left')
        self.description_label.grid(row=1, column=0, columnspan=3)

        self.start_label = tk.Label(self, text='Start Date (YYYY-MM-DD format)')
        self.start_label.grid(row=2, column=0)

        self.start_entry = tk.Entry(self)
        self.start_entry.grid(row=2, column=1)

        self.text_area = tk.Text(self)

        self.vertical_scrollbar = tk.Scrollbar(self.text_area, orient='vertical')
        self.vertical_scrollbar.config(command=self.text_area.yview)
        self.vertical_scrollbar.pack(side='right', fill='y')

        self.text_area.config(state='disabled', yscrollcommand=self.vertical_scrollbar.set)
        self.text_area.grid(row=2, column=3, sticky='nsew')

        self.end_label = tk.Label(self, text='End Date (YYYY-MM-DD format)')
        self.end_label.grid(row=3, column=0)

        self.end_entry = tk.Entry(self)
        self.end_entry.grid(row=3, column=1)

        self.back_btn = tk.Button(self, text='Back',
                                  command=self.go_back)
        self.back_btn.grid(row=4, column=0)

        self.submit_btn = tk.Button(self, text='Submit',
                                    command=self.display_confirmation_prompt)
        self.submit_btn.grid(row=4, column=1)



        self.bill_listings = []

    def check_dates(self):
        error_color = '#ff9a8c'

        # start_date = None
        self.start_entry.config(background='white')
        try:
            start_date = date.fromisoformat(self.start_entry.get())
        except ValueError as e:
            print(e)
            self.start_entry.config(background=error_color)
            return None, None

        # end_date = None
        self.end_entry.config(background='white')
        try:
            end_date = date.fromisoformat(self.end_entry.get())
        except ValueError as e:
            print(e)
            self.end_entry.config(background=error_color)
            return None, None

        if start_date is None or end_date is None:
            return None, None

        if end_date < start_date:
            self.end_entry.config(background=error_color)
            return None, None

        return start_date, end_date

    def display_confirmation_prompt(self):
        start_date, end_date = self.check_dates()
        if not start_date and not end_date:
            return

        listings = self.yield_bill_listings(start_date, end_date)
        listing_of_bills = [x for x in listings]
        count = len(listing_of_bills)
        answer = messagebox.askokcancel(title="continue?", message=f'You are about to download at most {count} files.  '
                                                                   f'Do you wish to continue?')
        if not answer:
            return

        self.process_bills(listing_of_bills)

    def process_bills(self, listing):
        self.text_area.delete(1.0, tk.END)
        trainer = TrainingController(self.datasource)
        trainer.train_model(listing)

    def yield_bill_listings(self, start_date, end_date):
        return self.datasource.yield_list_of_bill_ids(start_date, end_date)

    def go_back(self):
        from Views.tk_start_page import StartPage
        self.master.switch_frame(StartPage)


