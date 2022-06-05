import tkinter as tk

from Views.tk_start_page import StartPage


class TKInterInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.window.geometry('300x300')
        self._frame = None
        self.switch_frame(StartPage)

    # https://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
    def switch_frame(self, frame_class):
        # Destroys current frame and replaces it with a new one.
        if self._frame is not None:
            self._frame.destroy()
        self._frame = frame_class(self)
        self._frame.pack()

    def exit_program(self):
        self.window.destroy()

    def run(self):
        self.mainloop()
        self.switch_frame(StartPage)


class TrainPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.title('billspy -- Train Model')