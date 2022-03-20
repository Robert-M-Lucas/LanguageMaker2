from tkinter import *
from Database.Database import Database
from .WordSelector import WordSelector
from .SynonymManager import SynonymManager
from .WordManager import WordManager
from Translator import Translate


class MainGui:
    def __init__(self, lang):
        self.database = Database(lang)

        self.master = Tk()
        self.master.title("Language Maker 2 - " + lang)
        self.root = Frame(self.master)
        self.root.pack()

        Button(self.root, text="Word Manager", command=lambda: WordSelector(self, lang)).pack(fill=X)

        self.mid_frame = Frame(self.root)
        self.mid_frame.pack()

        self.left = Frame(self.mid_frame)
        self.left.grid(row=0, column=0)
        self.right = Frame(self.mid_frame)
        self.right.grid(row=0, column=1)

        Label(self.left, text="Text in").pack()
        self.text_in = Text(self.left, width=40, height=15)
        self.text_in.pack()

        Label(self.right, text="Translated text").pack()
        self.trans_text = Text(self.right, width=40, height=15)
        self.trans_text.pack()

        Button(self.left, text=f"English to {lang}", command=self.translate_lang).pack(fill=X)
        Button(self.right, text=f"{lang} to English", command=self.translate_eng).pack(fill=X)

        self.master.mainloop()

    def translate_eng(self):
        self.trans_text.delete('1.0', END)
        self.trans_text.insert('1.0', Translate(self.text_in.get("1.0", END), self.database, True))

    def translate_lang(self):
        self.trans_text.delete('1.0', END)
        self.trans_text.insert('1.0', Translate(self.text_in.get("1.0", END), self.database, False))
