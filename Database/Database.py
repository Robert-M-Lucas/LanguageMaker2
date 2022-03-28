import sqlite3
from typing import List
from os import listdir
from os.path import isfile, join

from .Word import Word
from .DatabaseExceptions import WordNotFoundError


def GetLanguageList() -> List[str]:
    return [f.split(".")[0] for f in listdir("Data") if isfile(join("Data", f))]


class Database:
    def __init__(self, language: str):
        self.con = sqlite3.connect("Data/" + language + ".db")
        self.cur = self.con.cursor()

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

    def AddWord(self, word_name: str, phonetic_eng: str = "", description: str = "", lang_synonyms: List[str] = (), eng_synonyms: List[str] = ()):
        print(f"\nCreating word: {word_name}")

        self.cur.execute('INSERT INTO Words VALUES (?, ?, ?)',
                         (word_name, phonetic_eng, description))

        for s in lang_synonyms:
            self.cur.execute('INSERT INTO WordSynLang VALUES (?, ?)',
                             (word_name, s))

        for s in eng_synonyms:
            self.cur.execute('INSERT INTO WordSynEng VALUES (?, ?)',
                             (word_name, s))

        self.con.commit()

    def UpdateWordDB(self, word_name: str, phonetic_eng: str = "", description: str = "", lang_synonyms: List[str] = "", eng_synonyms: List[str] = ""):
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

    def UpdateWord(self, word: Word):
        print(f"\nUpdating word:\n{word}")

        if word.new_name != word.name:
            self.DeleteWord(word.name)
            self.AddWord(word.new_name, word.phonetic_eng, word.description, word.lang_synonyms, word.eng_synonyms)
        else:
            self.UpdateWordDB(word.name, word.phonetic_eng, word.description, word.lang_synonyms, word.eng_synonyms)

    def DeleteWord(self, word_name: str):
        print(f"Updating word: {word_name}")
        self.cur.execute('DELETE FROM Words WHERE WordName=:word', {"word": word_name})
        self.cur.execute('DELETE FROM WordSynEng WHERE WordName=:word', {"word": word_name})
        self.cur.execute('DELETE FROM WordSynLang WHERE WordName=:word', {"word": word_name})
        self.con.commit()

    def GetWord(self, word_name: str) -> Word:
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
        self.cur.execute('SELECT WordName FROM Words')
        out = self.cur.fetchall()

        return [n[0] for n in out]

    def GetAllWords(self) -> List[Word]:
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
        self.cur.execute('SELECT WordName FROM WordSynEng WHERE EngSyn = ?', (eng_word,))
        out = self.cur.fetchall()
        return [o[0] for o in out]

    def GetEngTrans(self, lang_word: str) -> List[str]:
        self.cur.execute('SELECT EngSyn FROM WordSynEng WHERE WordName = ?', (lang_word,))
        out = self.cur.fetchall()
        return [o[0] for o in out]
