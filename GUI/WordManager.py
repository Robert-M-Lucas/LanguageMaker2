from tkinter import *
from .SynonymManager import SynonymManager
from .HelpWindow import HelpWindow


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
        self.word_name_eng_str = StringVar(self.top, value=self.word.phonetic_eng)
        Entry(self.left, textvariable=self.word_name_eng_str).pack(fill=X)
        Label(self.left, text=f"'{lang}' synonyms").pack(fill=X)
        Button(self.left, text="Synonym manager", command=lambda: SynonymManager(self, lang)).pack(fill=X)
        Label(self.left, text=f"English synonyms").pack(fill=X)
        Button(self.left, text="Synonym manager", command=lambda: SynonymManager(self, "")).pack(fill=X)

        # RIGHT
        Label(self.right, text="Description").pack(fill=X)
        self.desc_text = Text(self.right, height=8, width=40)
        self.desc_text.insert(END, self.word.description)
        self.desc_text.pack(fill=BOTH)
        self.save_btn = Button(self.right, text="Save", command=self.save)
        self.save_btn.pack(fill=X)

    def save(self):
        self.word.new_name = self.word_name_str.get()
        self.word.phonetic_eng = self.word_name_eng_str.get()
        desc_text = self.desc_text.get("1.0", END)
        if desc_text[-1] == "\n":
            desc_text = desc_text[:-1]
        self.word.description = desc_text
        self.main_gui.database.UpdateWord(self.word)
        self.save_btn.configure(text="Saved")
        self.top.after(2000, lambda: self.save_btn.configure(text="Save"))

    def on_closing(self):
        self.word_selector.update_words()
        self.word_selector.top.deiconify()
        self.top.destroy()