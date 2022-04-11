import os
import sqlite3
from typing import List
from os import listdir
from os.path import isfile, join, isdir

from .Word import Word
from .DatabaseExceptions import WordNotFoundError, WordAlreadyExistsError, WordNameChangeReferenceError
from logger import *


def GetLanguageList() -> List[str]:
    DatabaseLog("Getting list of languages...")
    if not isdir("Data"):
        DatabaseLog("Directory 'Data' does not exist. Creating now", 1)
        os.mkdir("Data")
    return [f.split(".")[0] for f in listdir("Data") if isfile(join("Data", f))]


class Database:
    def __init__(self, language: str):
        self.con = sqlite3.connect("Data/" + language + ".db")
        self.cur = self.con.cursor()

        DatabaseLog(f"Database connected to {'Data/' + language + '.db'}")

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Words
                         (WordName TEXT PRIMARY KEY NOT NULL, 
                         PhoneticEng TEXT,
                         Description TEXT)
                        ''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS WordSynEng
                         (WordName TEXT NOT NULL, 
                         EngSyn TEXT NOT NULL,
                         PRIMARY KEY (WordName, EngSyn))
                        ''')

        self.cur.execute('''CREATE TABLE IF NOT EXISTS WordSynLang
                         (WordName TEXT NOT NULL, 
                         LangSyn TEXT NOT NULL,
                         PRIMARY KEY (WordName, LangSyn))
                        ''')

        self.con.commit()

        DatabaseLog("Tables created")

    def AddWord(self, word_name: str, phonetic_eng: str = "", description: str = "", lang_synonyms: List[str] = (),
                eng_synonyms: List[str] = ()):
        DatabaseLog(f"Creating word '{word_name}'")

        self.cur.execute('INSERT INTO Words VALUES (?, ?, ?)',
                         (word_name, phonetic_eng, description))

        for s in lang_synonyms:
            self.cur.execute('INSERT INTO WordSynLang VALUES (?, ?)',
                             (word_name, s))

        for s in eng_synonyms:
            self.cur.execute('INSERT INTO WordSynEng VALUES (?, ?)',
                             (word_name, s))

        self.con.commit()

    def UpdateWordDB(self, word_name: str, phonetic_eng: str = "", description: str = "", lang_synonyms: List[str] = "",
                     eng_synonyms: List[str] = ""):

        DatabaseLog(f"Updating word data for '{word_name}'")

        self.cur.execute('''UPDATE Words Set PhoneticEng = ?,
                          Description = ?
                          WHERE WordName = ?''',
                         (phonetic_eng, description, word_name))

        # Language synonyms
        lang_syns_to_add = lang_synonyms.copy()
        self.cur.execute('SELECT LangSyn FROM WordSynLang WHERE WordName = ?', (word_name,))
        out = self.cur.fetchall()

        to_remove = []
        for syn in out:
            if syn[0] in lang_synonyms:
                lang_syns_to_add.remove(syn[0])
            else:
                to_remove.append(syn[0])

        for r in to_remove:
            self.cur.execute('DELETE FROM WordSynLang WHERE WordName = ? AND LangSyn = ?', (word_name, r))

        for a in lang_syns_to_add:
            self.cur.execute('INSERT INTO WordSynLang VALUES (?, ?)', (word_name, a))

        # English synonyms
        eng_syns_to_add = eng_synonyms.copy()
        self.cur.execute('SELECT EngSyn FROM WordSynEng WHERE WordName = ?', (word_name,))
        out = self.cur.fetchall()

        to_remove = []
        for syn in out:
            if syn[0] in eng_synonyms:
                eng_syns_to_add.remove(syn[0])
            else:
                to_remove.append(syn[0])

        for r in to_remove:
            self.cur.execute('DELETE FROM WordSynEng WHERE WordName = ? AND EngSyn = ?', (word_name, r))

        for a in eng_syns_to_add:
            self.cur.execute('INSERT INTO WordSynEng VALUES (?, ?)', (word_name, a))

        self.con.commit()

    def ChangeWordName(self, old_name: str, new_name: str):
        DatabaseLog(f"Changing word name '{old_name}' to '{new_name}'")

        try:
            self.GetWord(new_name)
            raise WordAlreadyExistsError
        except WordNotFoundError:
            pass

        self.cur.execute("UPDATE Words SET WordName = ? WHERE WordName = ?", (new_name, old_name))

        self.cur.execute("UPDATE WordSynEng SET WordName = ? WHERE WordName = ?", (new_name, old_name))

        self.cur.execute("UPDATE WordSynLang SET WordName = ? WHERE WordName = ?", (new_name, old_name))

        try:
            self.cur.execute("UPDATE WordSynLang SET LangSyn = ? WHERE LangSyn = ?", (new_name, old_name))
            integrity_error = False
        except sqlite3.IntegrityError:
            integrity_error = True

        self.con.commit()

        if integrity_error:
            DatabaseLog(f"Integrity error when changing word name", 2)
            raise WordNameChangeReferenceError

    def UpdateWord(self, word: Word):
        DatabaseLog(f"Updating word '{word.name}'")

        if word.new_name != word.name:
            self.ChangeWordName(word.name, word.new_name)
            word.name = word.new_name
            self.UpdateWordDB(word.new_name, word.phonetic_eng, word.description, word.lang_synonyms, word.eng_synonyms)
        else:
            self.UpdateWordDB(word.name, word.phonetic_eng, word.description, word.lang_synonyms, word.eng_synonyms)

    def DeleteWord(self, word_name: str):
        DatabaseLog(f"Deleting word '{word_name}'")
        self.cur.execute('DELETE FROM Words WHERE WordName=:word', {"word": word_name})
        self.cur.execute('DELETE FROM WordSynEng WHERE WordName=:word', {"word": word_name})
        self.cur.execute('DELETE FROM WordSynLang WHERE WordName=:word', {"word": word_name})
        self.con.commit()

    def GetWord(self, word_name: str) -> Word:
        DatabaseLog(f"Getting word data for '{word_name}'")
        self.cur.execute('SELECT * FROM Words WHERE WordName=:word', {"word": word_name})
        word_out = self.cur.fetchall()

        if len(word_out) == 0:
            raise WordNotFoundError

        self.cur.execute('SELECT EngSyn FROM WordSynEng WHERE WordName=:word', {"word": word_name})
        eng_syn_out = self.cur.fetchall()

        self.cur.execute('SELECT LangSyn FROM WordSynLang WHERE WordName=:word', {"word": word_name})
        lang_syn_out = self.cur.fetchall()

        return Word(word_out[0], eng_syn_out, lang_syn_out)

    def GetAllWordNames(self) -> List[str]:
        DatabaseLog("Getting all word names")
        self.cur.execute('SELECT WordName FROM Words')
        out = self.cur.fetchall()

        return [n[0] for n in out]

    def GetAllWords(self) -> List[Word]:
        DatabaseLog("Getting all word data - This is usually slow and should be avoided", 1)
        self.cur.execute('SELECT * FROM Words')
        out = self.cur.fetchall()

        word_list = []
        for word in out:
            self.cur.execute('SELECT EngSyn FROM WordSynEng WHERE WordName=:word', {"word": word[0]})
            eng_syn_out = self.cur.fetchall()

            self.cur.execute('SELECT LangSyn FROM WordSynLang WHERE WordName=:word', {"word": word[0]})
            lang_syn_out = self.cur.fetchall()

            word_list.append(Word(word, eng_syn_out, lang_syn_out))

        return word_list

    def GetLangTrans(self, eng_word: str) -> List[str]:
        DatabaseLog(f"Getting lang translation for '{eng_word}'")
        self.cur.execute('SELECT WordName FROM WordSynEng WHERE EngSyn = ?', (eng_word,))
        out = self.cur.fetchall()
        return [o[0] for o in out]

    def BackSearchLangSyn(self, lang_syn: str):
        DatabaseLog(f"Getting lang synonyms for '{lang_syn}'")
        self.cur.execute('SELECT WordName FROM WordSynLang WHERE LangSyn = ?', (lang_syn,))
        out = self.cur.fetchall()
        return [o[0] for o in out]

    def GetEngTrans(self, lang_word: str) -> List[str]:
        DatabaseLog(f"Getting English translation for '{lang_word}'")
        self.cur.execute('SELECT EngSyn FROM WordSynEng WHERE WordName = ?', (lang_word,))
        out = self.cur.fetchall()
        return [o[0] for o in out]
