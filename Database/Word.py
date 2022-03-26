

class Word:
    def __init__(self, word_data, eng_syn_data, lang_syn_data):
        self.name = word_data[0]
        self.new_name = None
        self.phonetic_eng = word_data[1]
        self.description = word_data[2]

        self.lang_synonyms = [s[0] for s in lang_syn_data]
        self.eng_synonyms = [s[0] for s in eng_syn_data]

    def __str__(self):
        _str = f"""Name: {self.name}
New Name: {self.new_name}
Phonetic English: {self.phonetic_eng}
Description: {self.description}
Lang Synonyms: {self.lang_synonyms}
English Synonyms: {self.eng_synonyms}"""
        return _str
