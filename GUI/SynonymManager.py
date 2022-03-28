from .HelpWindow import HelpWindow

from itertools import chain
from tkinter import *
from nltk.corpus import wordnet


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
        self.curr_synonyms = StringVar(self.top, value=self.syn_list)
        self.curr_lb = Listbox(self.left, listvariable=self.curr_synonyms)
        self.curr_lb.pack(fill=X)
        Button(self.left, text="Delete", command=self.delete).pack(fill=X)

        # RIGHT
        Label(self.right, text="Suggested Synonyms").pack(fill=X)
        self.suggested_list = []
        self.suggested = StringVar(self.top)
        self.sugg_lb = Listbox(self.right, listvariable=self.suggested)
        self.sugg_lb.pack(fill=X)
        self.sugg_lb.bind('<<ListboxSelect>>', self.select)

        self.entry_frame = Frame(self.right)
        self.entry_frame.pack(fill=X)
        self.new_syn = StringVar(self.top)
        Entry(self.entry_frame, textvariable=self.new_syn).grid(row=0, column=0)
        Button(self.entry_frame, text="Add", command=self.add_syn).grid(row=0, column=1)

        self.update_synonyms()

    def select(self, *args):
        self.new_syn.set(self.suggested_list[self.sugg_lb.curselection()[0]])

    def delete(self):
        self.syn_list.pop(self.curr_lb.curselection()[0])
        self.curr_syns_update()
        self.update_synonyms()

    def add_syn(self):
        self.syn_list.append(self.new_syn.get())
        self.curr_syns_update()
        self.update_synonyms()

    def curr_syns_update(self):
        self.curr_synonyms.set(self.syn_list)

    def update_synonyms(self):
        synonyms_dict = {}

        if self.mode == "":
            for curr_syn in self.syn_list:
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

        # TODO: This code can be greatly optimised
        else:
            all_words = self.word_manager.main_gui.database.GetAllWords()

            for word in all_words:
                for w in word.lang_synonyms:
                    wl = w
                    if wl == word.name or wl in self.syn_list or wl == self.word_manager.word.name:
                        continue
                    if wl not in synonyms_dict.keys():
                        synonyms_dict[wl] = 0
                    else:
                        synonyms_dict[wl] += 1

        self.suggested_list = sorted(synonyms_dict.keys(), key=synonyms_dict.get)
        self.suggested_list.reverse()
        self.suggested.set(self.suggested_list)
