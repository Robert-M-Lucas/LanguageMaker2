from tkinter import *
from Database.Database import Database
from .WordSelector import WordSelector
from .MainGuiTranslation import MainGuiTranslation
from .HelpWindow import HelpWindow

# from .SynonymManager import SynonymManager
# from .WordManager import WordManager
# from Translator import TranslateAll, Translator, TranslationStep
# from .InputPopup import InputPopup


class MainGui(MainGuiTranslation):
    def __init__(self, lang):
        self.database = Database(lang)

        self.master = Tk()
        self.master.title(f"Language Maker 2 - '{lang}'")
        self.root = Frame(self.master)
        self.root.pack(fill=X, expand=1)

        HelpWindow(self.master, "MainGui")

        Button(self.root, text="Word Manager", command=lambda: WordSelector(self, lang)).pack(fill=X, expand=1)

        self.mid_frame = Frame(self.root)
        self.mid_frame.pack(fill=X, expand=1)

        self.left = Frame(self.mid_frame)
        self.left.grid(row=0, column=0, sticky=N+E+S+W)
        self.right = Frame(self.mid_frame)
        self.right.grid(row=0, column=1, sticky=N+E+S+W)

        Label(self.left, text="Text in").pack(fill=X, expand=1)
        self.text_in = Text(self.left, width=40, height=15)
        self.text_in.pack(fill=X, expand=1)

        Label(self.right, text="Translated text").pack(fill=X, expand=1)
        self.trans_text = Text(self.right, width=40, height=15)
        self.trans_text.pack(fill=X, expand=1)

        self.left_bottom = Frame(self.left)
        self.left_bottom.pack(fill=X, expand=1)
        self.left_bottom.rowconfigure(0, weight=1)
        self.left_bottom.columnconfigure(0, weight=1)
        self.left_bottom.columnconfigure(1, weight=1)

        Button(self.left_bottom, text=f"{lang} to English", command=lambda: self.translate(True))\
            .grid(row=0, column=0, sticky=N+E+S+W)
        Button(self.left_bottom, text=f"{lang} to English Phonetic", command=self.translate_phonetic) \
            .grid(row=0, column=1, sticky=N+E+S+W)

        self.right_bottom = Frame(self.right)
        self.right_bottom.pack(fill=X, expand=1)

        Button(self.right_bottom, text=f"English to {lang}", command=lambda: self.translate(False), width=30) \
            .grid(row=0, column=0, sticky=N + E + S + W)
        self.deterministic = IntVar()
        Checkbutton(self.right_bottom, text="Stepped", variable=self.deterministic, width=10).grid(row=0, column=1)

        self.translator = None
        self.trans_top = None
        self.trans_top_root = None

        self.master.mainloop()


