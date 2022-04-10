from tkinter import *


class TextWithPlaceholder(Text):
    def __init__(self, master, placeholder: str, **kwargs):
        self.placeholder = placeholder
        super().__init__(master, **kwargs)

        self.placeholder_color = 'grey'

        self.placeholder_in = False

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.after(1, self.foc_out)

    def get(self, *args):
        if self.placeholder_in:
            return "\n"
        else:
            return super().get(*args)

    def insert(self, *args) -> None:
        if self.placeholder_in:
            self.remove_placeholder()
        super().insert(*args)

    def place_placeholder(self):
        self.insert(END, self.placeholder)
        self['fg'] = self.placeholder_color
        self.placeholder_in = True

    def remove_placeholder(self):
        self.placeholder_in = False
        self.delete('1.0', END)
        self['fg'] = "black"

    def foc_in(self, *args):
        if self.placeholder_in:
            self.remove_placeholder()

    def foc_out(self, *args):
        if not self.placeholder_in and self.get('1.0', END) == "" or self.get('1.0', END) == "\n":
            self.place_placeholder()
