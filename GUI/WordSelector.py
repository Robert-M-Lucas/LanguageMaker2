from tkinter import *
from tkinter import messagebox

from .InputPopup import InputPopup
from .WordManager import WordManager
from .HelpWindow import HelpWindow

from Translator import PUNCTUATION
from logger import *
from Extensions.EntryWithPlaceholder import EntryWithPlaceholder


class WordSelector:
    def __init__(self, main_gui, lang, single_select=False, single_select_callback=None):
        self.single_select_callback = single_select_callback
        self.lang = lang
        self.current_word_name_list = main_gui.database.GetAllWordNames()
        self.main_gui = main_gui
        self.top = Toplevel(main_gui.master)
        self.top.grab_set()
        self.default_title = "Word Selector"
        self.top.title(self.default_title)
        self.top.resizable(False, False)

        HelpWindow(self.top, "WordSelector")

        self.entry_frame = Frame(self.top)
        self.entry_frame.pack(fill=X)
        self.search_entry = EntryWithPlaceholder(self.entry_frame, "Search...")
        self.search_entry.grid(row=0, column=0)
        Button(self.entry_frame, text="🔎", command=self.search).grid(row=0, column=1)

        self.lbf = Frame(self.top)
        self.lbf.pack(fill=BOTH, expand=1)
        self.lb_var = StringVar(value=self.current_word_name_list)
        self.lb = Listbox(self.lbf, listvariable=self.lb_var)
        self.lb.pack(fill=X, side=LEFT)
        sb = Scrollbar(self.lbf, command=self.lb.yview)
        sb.pack(fill=Y, expand=1)
        self.lb.config(yscrollcommand=sb.set)

        if single_select:
            Button(self.top, text="Select word", command=self.select_word).pack(fill=X)

        Button(self.top, text="Edit selected word", command=self.edit_word).pack(fill=X)
        Button(self.top, text="Delete selected word", command=self.delete_word).pack(fill=X)
        b = Button(self.top, text="Create new word", command=self.get_new)
        b.pack(fill=X)
        b.focus_set()

    def get_new(self):
        InputPopup(self.top, self.create_word, "Enter new word name:", True)

    def select_word(self, word=None):
        if word is None:
            word = self.current_word_name_list[self.lb.curselection()[0]]
        self.top.destroy()
        self.single_select_callback(word)


    def create_word(self, word_name: str):
        word_name = word_name.replace(" ", "_")

        for c in PUNCTUATION:
            if c in word_name:
                messagebox.showerror("Illegal character in word name", "Word name cannot contain punctuation or "
                                                                       "special characters other than '_'")
                return

        for w in self.current_word_name_list:
            if word_name == w:
                messagebox.showerror("Word already", f"Word '{word_name}' already exists")
                self.edit_word(word_name)
                return

        self.main_gui.database.AddWord(word_name)

        self.update_words()
        self.edit_word(word_name)

    def update_words(self, query=None):
        self.current_word_name_list = self.main_gui.database.GetAllWordNames()

        if query is not None and query != "":
            x = 0
            while x < len(self.current_word_name_list):
                if query.upper() in self.current_word_name_list[x].upper():
                    x += 1
                else:
                    self.current_word_name_list.pop(x)

        self.lb_var.set(value=self.current_word_name_list)

    def delete_word(self):
        word = self.current_word_name_list[self.lb.curselection()[0]]

        msg_box = messagebox.askquestion('Delete word?', f"Are you sure you want to delete '{word}'",
                                         icon='warning')

        if msg_box == 'no':
            return

        self.main_gui.database.DeleteWord(word)
        self.update_words()

    def edit_word(self, word=None):
        if word is None:
            word = self.current_word_name_list[self.lb.curselection()[0]]
        WordManager(self.top, self.main_gui, self, self.lang, word)
        self.top.withdraw()

    def search(self):
        self.update_words(query=self.search_entry.get())
        if self.search_entry.get() == "":
            self.top.title(self.default_title)
        else:
            self.top.title(f"Search for '{self.search_entry.get()}'")
