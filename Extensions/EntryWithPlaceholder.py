import tkinter as tk


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master, placeholder, text="", **kwargs):
        self.textvariable = tk.StringVar()
        self.textvariable.set(text)

        super().__init__(master, textvariable=self.textvariable,  **kwargs)

        color = 'grey'



        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        if super().get() == "":
            self.put_placeholder()

    def get(self) -> str:
        potential_return = self.textvariable.get()

        if potential_return == self.placeholder:
            return ""
        else:
            return potential_return

    def set(self, text):
        self.textvariable.set(text)

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
