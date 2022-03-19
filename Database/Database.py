import sqlite3
from .Word import Word, WordAttributes
from .DatabaseExceptions import WordNotFoundError
from typing import List
from os import listdir
from os.path import isfile, join


def GetLanguageList() -> List[str]:
    return [f.split(".")[0] for f in listdir("Data") if isfile(join("Data", f))]


class Database:
    def __init__(self, language: str):
        self.con = sqlite3.connect("Data/" + language + ".db")
        self.cur = self.con.cursor()

        self.cur.execute('''CREATE TABLE IF NOT EXISTS Words
                         (WordName TEXT PRIMARY KEY NOT NULL, 
                         ''' +
                         ",".join(WordAttributes().attr) +
                         ''')''')

        self.con.commit()

    def AddWord(self, word_name: str, phonetic_eng: str = "", description: str = "", lang_synonyms: List[str] = "", eng_synonyms: List[str] = ""):
        self.cur.execute('INSERT INTO Words VALUES (?, ?, ?, ?, ?)',
                         (word_name, phonetic_eng, description, ";".join(lang_synonyms), ";".join(eng_synonyms)))
        self.con.commit()

    def UpdateWordDB(self, word_name: str, phonetic_eng: str = "", description: str = "", lang_synonyms: List[str] = "", eng_synonyms: List[str] = ""):
        self.cur.execute('''UPDATE Words Set PhoneticEng = ?,
                          Description = ?,
                          LangSynonyms = ?,
                          EngSynonyms = ?
                          WHERE WordName = ?''',
                         (phonetic_eng, description, ";".join(lang_synonyms), ";".join(eng_synonyms), word_name))
        self.con.commit()

    def UpdateWord(self, word: Word):
        if word.new_name != word.name:
            self.DeleteWord(word.name)
            self.AddWord(word.new_name, word.phonetic_eng, word.description, word.lang_synonyms, word.eng_synonyms)
        else:
            self.UpdateWordDB(word.name, word.phonetic_eng, word.description, word.lang_synonyms, word.eng_synonyms)

    def DeleteWord(self, word_name: str):
        self.cur.execute('DELETE FROM Words WHERE WordName=:word', {"word": word_name})
        self.con.commit()

    def GetWord(self, word_name: str) -> Word:
        print(word_name)
        print(type(word_name))
        self.cur.execute('SELECT * FROM Words WHERE WordName=:word', {"word": word_name})
        out = self.cur.fetchall()

        if len(out) == 0:
            raise WordNotFoundError

        return Word(out[0])

    def GetAllWords(self) -> List[Word]:
        self.cur.execute('SELECT * FROM Words')
        out = self.cur.fetchall()
        word_list = []
        for word in out:
            word_list.append(Word(word))

        return word_list
