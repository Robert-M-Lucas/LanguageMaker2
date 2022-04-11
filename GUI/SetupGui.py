from nltk_util import download
from tkinter import messagebox
import os
import shutil

# import tkinter as tk
# from tkinter.constants import *
# from tkinter.ttk import *

from tkinter import *
from tkinter import ttk

from .InputPopup import InputPopup
from .MainGui import MainGui
from .HelpWindow import HelpWindow

from Database.Database import GetLanguageList
import utils
from logger import *

# TODO: All file management should be done from Database.py


class SetupGui:
    def __init__(self, has_nltk: bool):
        self.exit = True
        self.has_nltk = has_nltk
        self.master = Tk()
        self.master.title("Pick a language")
        self.master.protocol("WM_DELETE_WINDOW", utils.exit)
        self.master.iconbitmap(default='GUI/icon.ico')
        self.master.resizable(False, False)

        # style = Style(self.master)
        # style.theme_use("vista")

        with open("VERSION.txt", "r") as f:
            self.version = "v0." + f.read()

        self.top_frame = Frame(self.master)
        self.top_frame.pack()
        Label(self.top_frame, text="Language Maker 2").pack(fill=X, side=LEFT)
        Label(self.top_frame, text=self.version, foreground="grey").pack(fill=X, side=RIGHT)

        self.root = None
        self.lang_selected = StringVar()
        self.error_label = None

        self.reload_gui()

    def reload_gui(self):
        Log("SETUP", "Reloading")

        if self.root is not None:
            self.root.destroy()
        self.root = Frame(self.master)
        self.root.pack(fill=X, expand=1)

        HelpWindow(self.master, "SetupGui")

        if self.has_nltk:
            Label(self.root, text="NLTK Downloaded").pack(fill=X, expand=1, side=TOP)
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

            b = Button(self.root, text="Use this language", command=self.get_lang_from_select)
            b.focus_set()
            b.pack(fill=X)

            Button(self.root, text="Delete this language", command=self.delete_lang).pack(fill=X)
            Button(self.root, text="Duplicate this language", command=self.duplicate_lang).pack(fill=X)

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
                messagebox.showerror(f"Language creation error", f"Language '{lang}' already exists")
                return
        self.start_main_gui(lang)

    def get_lang_from_select(self):
        self.start_main_gui(self.lang_selected.get())

    def duplicate_lang(self):
        lang = self.lang_selected.get()
        InputPopup(self.master, lambda x: self.duplicate_lang_confirm(lang, x), f"Enter language name for\n'{lang}' "
                                                                                f"duplicate", lang)

    def duplicate_lang_confirm(self, lang, new_lang):
        for c in new_lang:
            if c.upper() not in utils.ALLOWED_LANG_CHARS:
                DatabaseLog(f"Language duplication error: Language name contained illegal character '{c}'", 2)
                messagebox.showerror("Language duplication error", f"Language name contained illegal character '{c}'")
                return

        db_files = [f.split(".")[0] for f in os.listdir("Data") if os.path.isfile(os.path.join("Data", f))]
        for db in db_files:
            if db.upper() == new_lang.upper():
                DatabaseLog(f"Language duplication error: Language '{new_lang}' already exists", 2)
                messagebox.showerror(f"Language duplication error", f"Language '{new_lang}' already exists")
                return

        try:
            shutil.copy(f"Data/{lang}.db", f"Data/{new_lang}.db")

            try:
                shutil.copy(f"Data/{lang}.dbdata", f"Data/{new_lang}.dbdata")
            except FileNotFoundError:
                DatabaseLog(f"Language '{lang}' has no dbdata file to copy", 1)

            DatabaseLog(f"Language '{lang}' duplicated (New name: '{new_lang}')")
            messagebox.showinfo("Success", f"Language '{lang}' duplicated")
            self.reload_gui()
        except Exception as e:
            DatabaseLog(f"Language duplication error: {e}")
            messagebox.showerror("Language duplication error", f"Error: {e}")
            self.reload_gui()

    def delete_lang(self):
        lang = self.lang_selected.get()
        InputPopup(self.master, self.delete_lang_confirm, f"Type '{lang}' to delete\n(case sensitive)", lang)

    def delete_lang_confirm(self, lang):
        if self.lang_selected.get() == lang:
            try:
                os.remove(f"Data/{lang}.db")

                try:
                    os.remove(f"Data/{lang}.dbdata")
                except FileNotFoundError:
                    DatabaseLog(f"Language '{lang}' has no dbdata file to delete", 1)

                DatabaseLog(f"Database '{lang}' deleted")
                messagebox.showinfo("Success", f"Language '{lang}' deleted")
                self.reload_gui()
            except Exception as e:
                DatabaseLog(f"Language '{lang}' deletion error: {e}", 2)
                messagebox.showerror("Language deletion error", f"Error: {e}")
                self.reload_gui()
        else:
            messagebox.showerror("Failed", f"Language '{self.lang_selected.get()}' did not match entry '{lang}'")

    def start_main_gui(self, lang):
        for l in lang:
            if l.upper() not in utils.ALLOWED_LANG_CHARS:
                self.error_label.config(text="Banned character in language name")
                return
        self.master.destroy()
        MainGui(lang, self)
        if self.exit:
            utils.exit()
