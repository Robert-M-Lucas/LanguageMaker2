class WordAttributes:
    def __init__(self):
        # WordName primary key
        # Synonyms ;-separated
        self.attr = ("PhoneticEng TEXT", "Description TEXT", "LangSynonyms TEXT", "EngSynonyms TEXT")


class Word:
    def __init__(self, db_data):
        self.name = db_data[0]
        self.new_name = ""
        self.phonetic_eng = db_data[1]
        self.description = db_data[2]
        self.lang_synonyms = db_data[3].split(";")
        self.eng_synonyms = db_data[4].split(";")

    def __str__(self):
        _str = f"""Name: {self.name}
New Name: {self.new_name}
Phonetic English: {self.phonetic_eng}
Description: {self.description}
Lang Synonyms: {self.lang_synonyms}
English Synonyms: {self.eng_synonyms}"""
        return _str