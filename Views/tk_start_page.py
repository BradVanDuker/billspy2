import tkinter as tk

from Views.tk_summary_page import SummaryPage


class StartPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.title('billspy - Main Menu')

        self.rowconfigure([0, 1, 2], weight=1, minsize=25)
        self.columnconfigure(0, weight=1, minsize=200)
        self.grid(column=0, row=0)

        get_summary_btn = tk.Button(self, justify='center', text='Get Summary',
                                    command=lambda: master.switch_frame(SummaryPage))
        get_summary_btn.grid(column=0, row=0, sticky='ew', padx=5, pady=5)

        train_btn = tk.Button(self, justify='center', text='Train')
        train_btn.grid(column=0, row=1, sticky='ew', padx=5, pady=5)

        exit_btn = tk.Button(self, justify='center', text='Exit', command=self.exit_program)
        exit_btn.grid(column=0, row=2, sticky='ew', padx=5, pady=5)

    def exit_program(self):
        self.destroy()
        self.master.destroy()

    def goto_get_summary_page(self):
        self.master.switch_frame(SummaryPage)
