from Database.Database import Database
from Database.Word import Word
from Database.Database import GetLanguageList
import os


os.remove("Data/new_lang.db")
db = Database("new_lang")
db.AddWord("x", "ay", "description here", ["b", "c"], ["a", "s"])
db.AddWord("b", "ay", "description here", ["b", "e"], ["a", "s"])
word = db.GetWord("b")
word.new_name = "c"
db.UpdateWord(word)
print(db.GetWord("c"))
print()
print(db.GetWord("x"))
