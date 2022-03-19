from Database.Database import Database
from Database.Word import Word
from Database.Database import GetLanguageList

print(GetLanguageList())

db = Database("new_lang")
db.AddWord("b", "ay", "description here", ["b", "c"], ["a", "s"])
db.AddWord("a", "ay", "description here", ["b", "c"], ["a", "s"])
print(db.GetAllWords())
