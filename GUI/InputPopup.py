from tkinter import *


class InputPopup:
    def __init__(self, master, callback, prompt: str = "Enter text"):
        self.callback = callback
        top = self.top = Toplevel(master)
        l = Label(top, text=prompt)
        l.pack()
        self.e = Entry(top)
        self.e.pack()
        b = Button(top, text='Submit', command=self.ret)
        b.pack()

    def ret(self):
        v = self.e.get()
        self.top.destroy()
        self.callback(v)
