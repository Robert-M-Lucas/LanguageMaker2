from tkinter import *
from nltk_util import download
from tkinter import ttk
from tkinter import messagebox
import os

from .InputPopup import InputPopup
from .MainGui import MainGui
from .HelpWindow import HelpWindow

from Database.Database import GetLanguageList
import utils


class SetupGui:
    def __init__(self, has_nltk: bool):
        self.has_nltk = has_nltk
        self.master = Tk()
        self.master.title("Pick a language")
        with open("VERSION.txt", "r") as f:
            self.version = f.read()

        self.top_frame = Frame(self.master)
        self.top_frame.pack()
        Label(self.top_frame, text="Language Maker 2").pack(fill=X, side=LEFT)
        Label(self.top_frame, text=self.version, fg="grey").pack(fill=X, side=RIGHT)

        self.root = None
        self.lang_selected = StringVar()
        self.error_label = None

        self.reload_gui()

    def reload_gui(self):
        if self.root is not None:
            self.root.destroy()
        self.root = Frame(self.master)
        self.root.pack(fill=X, expand=1)

        HelpWindow(self.master, "SetupGui")

        if self.has_nltk:
            Label(self.root, text="NLTK Downloaded").pack(fill=X, expand=1)
            Button(self.root, text="Re-Download", command=download).pack(fill=X, expand=1)
        else:
            Label(self.root, text="NLTK Not Downloaded\nSome functionality might be missing").pack(fill=X, expand=1)
            Button(self.root, text="Download", command=download).pack(fill=X, expand=1)

        ttk.Separator(self.root, orient=HORIZONTAL).pack(fill=X, pady=(4, 0))

        langs = GetLanguageList()

        if len(langs) > 0:
            self.lang_selected.set(langs[0])

            drop = OptionMenu(self.root, self.lang_selected, *langs)
            drop.pack(fill=X)

            Button(self.root, text="Use this language", command=self.get_lang_from_select).pack(fill=X)

            Button(self.root, text="Delete this language", command=self.delete_lang).pack(fill=X)

        Button(self.root, text="Create new language", command=self.create_lang).pack(fill=X)

        self.error_label = Label(self.root, text="You can press F1 for help\non most windows")
        self.error_label.pack(side=LEFT)

        # ttk.Separator(self.root, orient=HORIZONTAL).pack(fill=X)

        # Label(self.root, text=self.version, fg="grey").pack(fill=X, side=RIGHT)

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

    def delete_lang(self):
        lang = self.lang_selected.get()
        InputPopup(self.master, self.delete_lang_confirm, f"Type '{lang}' to delete", lang)

    def delete_lang_confirm(self, lang):
        if self.lang_selected.get() == lang:
            try:
                os.remove(f"Data/{lang}.db")
                self.reload_gui()
                messagebox.showinfo("Success", f"Language '{lang}' deleted")
            except Exception as e:
                messagebox.showerror("Language deletion error", f"Error: {e}")
                self.reload_gui()
        else:
            messagebox.showerror("Failed", f"Language '{self.lang_selected.get()}' didn't match entry '{lang}'")

    def start_main_gui(self, lang):
        for l in lang:
            if l.upper() not in utils.ALLOWED_LANG_CHARS:
                self.error_label.config(text="Banned character in language name")
                return
        self.master.destroy()
        MainGui(lang)
