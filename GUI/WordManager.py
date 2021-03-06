from tkinter import *
from tkinter import messagebox

from .SynonymManager import SynonymManager
from .HelpWindow import HelpWindow
from Extensions.EntryWithPlaceholder import EntryWithPlaceholder
from Extensions.TextWithPlaceholder import TextWithPlaceholder
from logger import *
from Translator import PUNCTUATION


class WordManager:
    def __init__(self, master, main_gui, word_selector, lang, word_name):
        self.word_name = word_name
        self.main_gui = main_gui
        self.word = main_gui.database.GetWord(word_name)
        self.word_selector = word_selector
        self.lang_synonyms = self.word.lang_synonyms
        self.eng_synonyms = self.word.eng_synonyms

        self.top = Toplevel(master)
        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.top.grab_set()
        self.top.title(f"Word Manager for {word_name}")
        self.top.resizable(False, False)

        HelpWindow(self.top, "WordManager")

        self.root = Frame(self.top)
        self.root.pack()

        self.left = Frame(self.root)
        self.left.grid(row=0, column=0)
        self.right = Frame(self.root)
        self.right.grid(row=0, column=1)

        # LEFT
        Label(self.left, text=f"Word in '{lang}'").pack(fill=X)
        self.word_name_str = StringVar(self.top, value=self.word.name)
        Entry(self.left, textvariable=self.word_name_str).pack(fill=X)
        Label(self.left, text=f"Word in phonetic English").pack(fill=X)
        self.word_name_eng_str = EntryWithPlaceholder(self.left, "Same as word name")
        self.word_name_eng_str.set(self.word.phonetic_eng)
        self.word_name_eng_str.pack(fill=X)
        Label(self.left, text=f"'{lang}' synonyms").pack(fill=X)
        Button(self.left, text="Synonym manager", command=lambda: SynonymManager(self, lang)).pack(fill=X)
        Label(self.left, text=f"English synonyms").pack(fill=X)
        Button(self.left, text="Synonym manager", command=lambda: SynonymManager(self, "")).pack(fill=X)

        # RIGHT
        Label(self.right, text="Description").pack(fill=X)
        self.desc_frm = Frame(self.right)
        self.desc_frm.pack(fill=X, expand=1)

        self.desc_text = TextWithPlaceholder(self.desc_frm, placeholder="Enter description here", height=8, width=40)
        self.desc_text.insert(END, self.word.description)
        self.desc_text.pack(side=LEFT, fill=BOTH)
        sb = Scrollbar(self.desc_frm, command=self.desc_text.yview)
        self.desc_text.config(yscrollcommand=sb.set)
        sb.pack(side=RIGHT, fill=Y)
        self.save_btn = Button(self.right, text="Save", command=self.save)
        self.save_btn.pack(fill=X)
        self.save_btn.focus_set()

    def save(self):
        for c in PUNCTUATION:
            if c in self.word_name_str.get():
                messagebox.showerror("NOT SAVED", "NOT SAVED: Word name cannot contain punctuation or "
                                                  "special characters other than '_'")
                return

        self.word.new_name = self.word_name_str.get()
        self.word.phonetic_eng = self.word_name_eng_str.get()
        desc_text = self.desc_text.get("1.0", END)
        if desc_text[-1] == "\n":
            desc_text = desc_text[:-1]
        self.word.description = desc_text
        self.main_gui.database.UpdateWord(self.word)
        self.save_btn.configure(text="Saved!")
        self.top.after(2000, lambda: self.save_btn.configure(text="Save"))

    def on_closing(self):
        self.word_selector.update_words()
        self.word_selector.top.deiconify()
        self.top.destroy()
