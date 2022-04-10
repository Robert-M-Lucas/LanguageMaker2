from tkinter import *

from Database.Database import Database
from .WordSelector import WordSelector
from .MainGuiTranslation import MainGuiTranslation
from .HelpWindow import HelpWindow
from Extensions.TextWithPlaceholder import TextWithPlaceholder


# from .SynonymManager import SynonymManager
# from .WordManager import WordManager
# from Translator import TranslateAll, Translator, TranslationStep
# from .InputPopup import InputPopup


class MainGui(MainGuiTranslation):
    def __init__(self, lang, setup_callback):
        self.database = Database(lang)
        self.setup_callback = setup_callback

        self.master = Tk()
        self.master.title(f"Language Maker 2 - '{lang}'")
        self.master.focus_force()
        self.master.resizable(False, False)
        self.root = Frame(self.master)
        self.root.pack(fill=BOTH, expand=1)

        HelpWindow(self.master, "MainGui")

        mid_frame = Frame(self.root)
        mid_frame.pack(fill=BOTH, expand=1)

        left = Frame(mid_frame)
        left.grid(row=0, column=0, sticky=N + E + S + W)
        right = Frame(mid_frame)
        right.grid(row=0, column=1, sticky=N + E + S + W)

        Button(left, text="Word Manager", command=lambda: WordSelector(self, lang)).pack(fill=X, expand=1)
        Label(left, text="Text in").pack(fill=X, expand=1)
        left_text = Frame(left)
        left_text.pack(fill=BOTH, expand=1)
        self.text_in = TextWithPlaceholder(left_text, placeholder="Type text to be translated here",
                                           width=45, height=20)
        self.text_in.pack(side=LEFT, fill=BOTH, expand=1)
        sbl = Scrollbar(left_text, command=self.text_in.yview)
        self.text_in.config(yscrollcommand=sbl.set)
        sbl.pack(side=RIGHT, fill=Y)

        Button(right, text="Return to language selection", command=self.return_to_setup).pack(fill=X, expand=1)
        Label(right, text="Translated text").pack(fill=X, expand=1)
        right_text = Frame(right)
        right_text.pack(fill=BOTH, expand=1)
        self.trans_text = TextWithPlaceholder(right_text, placeholder="Translated text will appear here",
                                              width=45, height=20)
        self.trans_text.pack(side=LEFT, fill=BOTH, expand=1)
        sbr = Scrollbar(right_text, command=self.trans_text.yview)
        self.trans_text.config(yscrollcommand=sbr.set)
        sbr.pack(side=RIGHT, fill=Y)

        left_bottom = Frame(left)
        left_bottom.pack(fill=X, expand=1)
        left_bottom.rowconfigure(0, weight=1)
        left_bottom.columnconfigure(0, weight=1)
        left_bottom.columnconfigure(1, weight=1)

        Button(left_bottom, text=f"'{lang}' to English", command=lambda: self.translate(True)) \
            .grid(row=0, column=0, sticky=N + E + S + W)
        Button(left_bottom, text=f"'{lang}' to English Phonetic", command=self.translate_phonetic) \
            .grid(row=0, column=1, sticky=N + E + S + W)

        right_bottom = Frame(right)
        right_bottom.pack(fill=X, expand=1)

        Button(right_bottom, text=f"English to '{lang}'", command=lambda: self.translate(False), width=30) \
            .grid(row=0, column=0, sticky=N + E + S + W)
        self.stepped = IntVar()
        Checkbutton(right_bottom, text="Stepped", variable=self.stepped, width=10).grid(row=0, column=1)

        self.translator = None
        self.trans_top = None
        self.trans_top_root = None

        self.master.mainloop()

    def return_to_setup(self):
        self.master.destroy()
        self.setup_callback.exit = False
