from itertools import chain
from tkinter import *
from tkinter import messagebox
from nltk.corpus import wordnet
import time

from .HelpWindow import HelpWindow
from Database.DatabaseExceptions import WordNotFoundError
from logger import *

MAX_SYNONYM_LOOKUP_TIME = 3


class SynonymManager:
    def __init__(self, word_manager, mode: str):
        self.mode = mode
        self.word_manager = word_manager
        if mode == "":
            window_name = "English Synonyms"
            self.syn_list = word_manager.word.eng_synonyms
        else:
            window_name = f"{mode} Synonyms"
            self.syn_list = word_manager.word.lang_synonyms

        self.top = Toplevel(word_manager.top)
        self.top.grab_set()
        self.top.title(window_name)

        HelpWindow(self.top, "SynonymManager")

        self.left = Frame(self.top)
        self.left.grid(row=0, column=0)
        self.right = Frame(self.top)
        self.right.grid(row=0, column=1)

        # LEFT
        Label(self.left, text="Current Synonyms").pack(fill=X)
        self.lb_l_f = Frame(self.left)
        self.lb_l_f.pack(fill=BOTH, expand=1)
        self.curr_synonyms = StringVar(self.top, value=self.syn_list)
        self.curr_lb = Listbox(self.lb_l_f, listvariable=self.curr_synonyms)
        self.curr_lb.pack(side=LEFT, fill=X)
        sbl = Scrollbar(self.lb_l_f, command=self.curr_lb.yview)
        sbl.pack(fill=Y, expand=1)
        self.curr_lb.config(yscrollcommand=sbl.set)
        Button(self.left, text="Delete", command=self.delete).pack(fill=X)

        # RIGHT
        Label(self.right, text="Suggested Synonyms").pack(fill=X)
        self.suggested_list = []
        self.suggested = StringVar(self.top)
        self.lb_r_f = Frame(self.right)
        self.lb_r_f.pack(fill=BOTH, expand=1)
        self.suggestion_lb = Listbox(self.lb_r_f, listvariable=self.suggested)
        self.suggestion_lb.pack(side=LEFT, fill=X)
        self.suggestion_lb.bind('<<ListboxSelect>>', self.select)
        sbr = Scrollbar(self.lb_r_f, command=self.suggestion_lb.yview)
        sbr.pack(fill=Y, expand=1)
        self.suggestion_lb.config(yscrollcommand=sbr.set)

        self.entry_frame = Frame(self.right)
        self.entry_frame.pack(fill=X)
        self.new_syn = StringVar(self.top)
        Entry(self.entry_frame, textvariable=self.new_syn).grid(row=0, column=0)
        Button(self.entry_frame, text="Add", command=self.try_add_syn).grid(row=0, column=1)

        self.update_synonyms()

    def select(self, *args):
        self.new_syn.set(self.suggested_list[self.suggestion_lb.curselection()[0]])

    def delete(self):
        self.syn_list.pop(self.curr_lb.curselection()[0])
        self.curr_syns_update()
        self.update_synonyms()

    def try_add_syn(self):
        new_syn = self.new_syn.get()

        if new_syn in self.syn_list:
            messagebox.showerror("Failed to add synonym", f"Synonym '{new_syn}' already a synonym")
            return

        if self.mode == "" and new_syn not in wordnet.words("eng"):
            msg_box = messagebox.askquestion('Word not english', f"Synonym '{new_syn}' not english. Add anyway?",
                                             icon='warning')
            if msg_box == 'no':
                return

        if self.mode != "":
            try:
                self.word_manager.main_gui.database.GetWord(new_syn)
            except WordNotFoundError:
                msg_box = messagebox.askquestion(f"Word not in '{self.mode}'",
                                                 f"Synonym '{new_syn}' not in language '{self.mode}'. Add anyway?",
                                                 icon='warning')
                if msg_box == 'no':
                    return

        self.add_syn(new_syn)

    def add_syn(self, syn):
        self.syn_list.append(syn)
        self.curr_syns_update()
        self.update_synonyms()

    def curr_syns_update(self):
        self.curr_synonyms.set(self.syn_list)

    def update_synonyms(self):
        SynManagerLog("Updating synonym predictions")
        synonyms_dict = {}

        if self.mode == "":
            start_time = time.time()

            for curr_syn in self.syn_list:
                if time.time() - start_time > MAX_SYNONYM_LOOKUP_TIME:
                    SynManagerLog(f"Synonym lookup time exceeded max lookup time ({MAX_SYNONYM_LOOKUP_TIME}s) ("
                                  f"English lookup)", 1)
                    break

                synonyms = wordnet.synsets(curr_syn)
                lemmas = set(chain.from_iterable([word.lemma_names() for word in synonyms]))
                for w in lemmas:
                    wl = w.lower()
                    if wl == curr_syn or wl in self.syn_list:
                        continue
                    if wl not in synonyms_dict.keys():
                        synonyms_dict[wl] = 0
                    else:
                        synonyms_dict[wl] += 1

        else:
            start_time = time.time()
            # Check if this word appears in any other words' synonym list
            words = self.word_manager.main_gui.database.BackSearchLangSyn(self.word_manager.word.name)
            for wl in words:
                if time.time() - start_time > MAX_SYNONYM_LOOKUP_TIME:
                    SynManagerLog(f"Synonym lookup time exceeded max lookup time ({MAX_SYNONYM_LOOKUP_TIME}s) ("
                                  f"Database Lookup)", 1)
                    break

                if wl not in synonyms_dict.keys():
                    synonyms_dict[wl] = 4
                else:
                    synonyms_dict[wl] += 5

            for i in self.syn_list:
                if time.time() - start_time > MAX_SYNONYM_LOOKUP_TIME:
                    SynManagerLog(f"Synonym lookup time exceeded max lookup time ({MAX_SYNONYM_LOOKUP_TIME}s) ("
                                  f"Database Lookup)", 1)
                    break

                words = self.word_manager.main_gui.database.BackSearchLangSyn(i)
                for wl in words:
                    if wl not in synonyms_dict.keys():
                        synonyms_dict[wl] = 0
                    else:
                        synonyms_dict[wl] += 1

        self.suggested_list = sorted(synonyms_dict.keys(), key=synonyms_dict.get)
        self.suggested_list.reverse()
        self.suggested.set(self.suggested_list)
