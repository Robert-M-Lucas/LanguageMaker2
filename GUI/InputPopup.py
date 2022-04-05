from tkinter import *
from typing import List


class InputPopup:
    def __init__(self, master, callback, prompt: str = "Enter text", blocking=False, callback_args: List = None):
        if callback_args is None:
            callback_args = []

        self.callback = callback
        self.callback_args = callback_args

        self.top = Toplevel(master)
        if blocking:
            self.top.grab_set()

        l = Label(self.top, text=prompt)
        l.pack(fill=X)

        self.e = Entry(self.top)
        self.e.pack(fill=X)
        self.e.focus_set()
        b = Button(self.top, text='Submit', command=self.ret)
        b.pack(fill=X)

    def ret(self):
        v = self.e.get()
        self.top.destroy()
        self.callback(v, *self.callback_args)
