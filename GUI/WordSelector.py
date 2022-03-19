from tkinter import *
from .InputPopup import InputPopup
from .WordManager import WordManager


class WordSelector:
    def __init__(self, main_gui, lang):
        self.lang = lang
        self.current_word_list = [word for word in main_gui.database.GetAllWords()]
        self.main_gui = main_gui
        self.top = Toplevel(main_gui.master)
        self.top.grab_set()
        self.top.title("Word Selector")

        self.entry_frame = Frame(self.top)
        self.entry_frame.pack(fill=X)
        Entry(self.entry_frame).grid(row=0, column=0)
        Button(self.entry_frame, text="🔎").grid(row=0, column=1)

        self.lb_var = StringVar(value=[word.name for word in self.current_word_list])
        self.lb = Listbox(self.top, listvariable=self.lb_var)
        self.lb.pack(fill=X)

        Button(self.top, text="Edit selected word", command=self.edit_word).pack(fill=X)
        Button(self.top, text="Delete selected word", command=self.delete_word).pack(fill=X)
        Button(self.top, text="Create new", command=self.get_new).pack(fill=X)

    def get_new(self):
        InputPopup(self.top, self.create_word, "Enter new word name:")

    def create_word(self, word_name):
        self.main_gui.database.AddWord(word_name)
        self.update_words()

    def update_words(self):
        self.current_word_list = [word for word in self.main_gui.database.GetAllWords()]
        self.lb_var.set(value=[word.name for word in self.current_word_list])

    def delete_word(self):
        self.main_gui.database.DeleteWord(self.current_word_list[self.lb.curselection()[0]].name)
        self.update_words()

    def edit_word(self):
        WordManager(self.top, self.main_gui, self, self.lang, self.current_word_list[self.lb.curselection()[0]].name)
        self.top.withdraw()

