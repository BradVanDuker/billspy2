import tkinter as tk
from datetime import date

from Models.apiDataSource import APIDataSource


class SummaryPage(tk.Frame):
    def __init__(self, master: tk.Tk):
        self.api_data_source = APIDataSource()
        self.seperator = ' -- ' # string that separates the bill number from the title

        super().__init__(master)
        master.title('billspy -- Summarize Bill')
        self.columnconfigure(0, minsize=50, pad=5)
        self.columnconfigure(1, minsize=50, pad=5)
        self.columnconfigure(2, minsize=50, pad=5)
        self.columnconfigure(3, minsize=50, pad=5)

        self.title_label = tk.Label(self, text='Summarize Bill')
        self.title_label.grid(row=0, column=0, columnspan=4)

        self.start_label = tk.Label(self, text='Start Date (YYYY-MM-DD format)')
        self.start_label.grid(row=1, column=0)

        self.start_entry = tk.Entry(self)
        self.start_entry.grid(row=1, column=1)

        self.end_label = tk.Label(self, text='End Date (YYYY-MM-DD format)')
        self.end_label.grid(row=2, column=0)

        self.end_entry = tk.Entry(self)
        self.end_entry.grid(row=2, column=1)

        self.back_btn = tk.Button(self, text='Back',
                                  command=self.go_back)
        self.back_btn.grid(row=3, column=0)

        self.search_btn = tk.Button(self, text='Search', command=self.populate_list_box)
        self.search_btn.grid(row=3, column=1)

        self.selected_bill = tk.StringVar()

        self.lb = tk.Listbox(self)

        self.lb_vertical_scrollbar = tk.Scrollbar(self.lb, orient='vertical')
        self.lb_vertical_scrollbar.config(command=self.lb.yview)
        self.lb_vertical_scrollbar.pack(side='right', fill='y')

        self.lb_horizontal_scrollbar = tk.Scrollbar(self.lb, orient='horizontal')
        self.lb_horizontal_scrollbar.config(command=self.lb.xview)
        self.lb_horizontal_scrollbar.pack(side='bottom', fill='x')

        self.lb.config(yscrollcommand=self.lb_vertical_scrollbar.set,
                       xscrollcommand=self.lb_horizontal_scrollbar.set)

        # self.lb.config(width=60)
        self.lb.grid(row=4, column=0, padx=5, pady=5, columnspan=2, sticky='nsew')

        # self.lb_vertical_scrollbar = tk.Scrollbar(self.lb, orient='vertical', command=self.lb.yview)
        # self.lb_vertical_scrollbar.pack(side='right', fill='y')
        # self.lb_horizontal_scrollbar = tk.Scrollbar(self.lb, orient='horizontal', command=self.lb.xview)
        # self.lb_horizontal_scrollbar.pack(side='bottom', fill='x')

        self.summarize_btn = tk.Button(self, text='Summarize',
                                       command=lambda: self.get_summary(self.get_user_selection(self.lb)))
        self.summarize_btn.grid(row=5, column=0, padx=5, pady=5)

        self.summarize_area = tk.Text(self)
        self.summarize_area.grid(row=1, column=2, padx=5, pady=5, rowspan=5)

    def populate_list_box(self):
        error_color = '#ff9a8c'

        start_date = None
        self.start_entry.config(background='white')
        try:
            start_date = date.fromisoformat(self.start_entry.get())
        except ValueError as e:
            print(e)
            self.start_entry.config(background=error_color)

        end_date = None
        self.end_entry.config(background='white')
        try:
            end_date = date.fromisoformat(self.end_entry.get())
        except ValueError as e:
            print(e)
            self.end_entry.config(background=error_color)

        if start_date is None or end_date is None:
            return

        if end_date < start_date:
            self.end_entry.config(background=error_color)
            return

        bills = self.api_data_source.get_bills_listing(start_date, end_date)

        for bill in bills:
            item_str = f'{bill["packageId"]}{self.seperator}{bill["title"]}'
            self.lb.insert(tk.END, item_str)

    def go_back(self):
        from Views.tk_start_page import StartPage
        self.master.switch_frame(StartPage)

    def get_summary(self, bill_id):
        # TODO:  throws an error if bill_id is not defined because no bill was selected in the list box.
        self.summarize_area.delete(1.0, 'end')
        self.summarize_area.insert(1.0, bill_id)

    def get_user_selection(self, list_box: tk.Listbox):
        selection = list_box.curselection()
        if len(selection) == 0:
            return

        selected_item = list_box.get(selection[0])
        print(selected_item)
        bill_id = selected_item.split(self.seperator)[0]

        return bill_id