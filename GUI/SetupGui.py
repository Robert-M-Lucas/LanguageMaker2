from tkinter import *
from nltk_util import download
from tkinter import ttk
import os

from .InputPopup import InputPopup
from .MainGui import MainGui
from .HelpWindow import HelpWindow


from Database.Database import GetLanguageList
import utils


class SetupGui:
    def __init__(self, has_nltk: bool):
        self.master = Tk()
        self.master.title("Pick a language")
        self.root = Frame(self.master)
        self.root.pack(fill=X, expand=1)

        HelpWindow(self.master, "SetupGui")

        if has_nltk:
            Label(self.root, text="NLTK Downloaded").pack(fill=X, expand=1)
            Button(self.root, text="Re-Download", command=download).pack(fill=X, expand=1)
        else:
            Label(self.root, text="NLTK Not Downloaded\nSome functionality might be missing").pack(fill=X, expand=1)
            Button(self.root, text="Download", command=download).pack(fill=X, expand=1)

        ttk.Separator(self.root, orient=HORIZONTAL).pack(fill=X, pady=3)

        self.langs = GetLanguageList()

        self.lang_selected = StringVar()
        if len(self.langs) > 0:
            self.lang_selected.set(self.langs[0])

            drop = OptionMenu(self.root, self.lang_selected, *self.langs)
            drop.pack(fill=X)

            Button(self.root, text="Use this language", command=self.get_lang_from_select).pack(fill=X)

        Button(self.root, text="Create new language", command=self.create_lang).pack(fill=X)

        self.error_label = Label(self.root, text="You can press F1 for help\non most windows")
        self.error_label.pack()

        self.master.mainloop()

    def create_lang(self):
        InputPopup(self.master, self.new_lang_check, "Enter new language name")

    def new_lang_check(self, lang):
        db_files = [f.split(".")[0] for f in os.listdir("Data") if os.path.isfile(os.path.join("Data", f))]
        for db in db_files:
            if db.upper() == lang.upper():
                self.error_label.config(text="Language already exists")
                return
        self.start_main_gui(lang)

    def get_lang_from_select(self):
        self.start_main_gui(self.lang_selected.get())

    def start_main_gui(self, lang):
        for l in lang:
            if l.upper() not in utils.ALLOWED_LANG_CHARS:
                self.error_label.config(text="Banned character in language name")
                return
        self.master.destroy()
        MainGui(lang)
