import requests
from pymystem3 import Mystem

URL = "http://web-corpora.net/Test2_2016/short_story.html"
RUSSIAN_ALPHABET = ['АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя']
data = requests.get(URL).content.decode()

def split_text(text, tokens):
    result = []
    start = 0
    end = 0
    while len(text) > 0 and end < len(text):
        if text[end] in tokens:
            result.append (text[start:end])
            text = text[end + 1:]
            start = 0
            end = 0
            continue
        end += 1
    return rusult

def get_words(text, startswith):
    result = []
    for word in split_text(data, " ,.!?:;\"'()<>/\\&\n"):
        if word and word[0] in startswith:
            result.append (word)
    return result

def get_speech_part(word, mystem):
    return mystem.analyze(word)[0]["analysis"][0]["gr"][0]

print("---------------Просто слова---------------")
for word in get_words(data, "сС"):
    print(word)

mystem = Mystem()
print("---------------Глаголы---------------")
for word in get_words(data, "сС"):
    if get_speech_part(word, mystem) == "V":
        print(word)

sql = "CREATE TABLE Words (`id` INTEGER PRIMARY KEY AUTOINCREMENT, `лемма` VARCHAR (100), `словоформа` VARCHAR (100), `часть речи` VARCHAR (100));\n"
for word in get_words(data, "сС"):
    sql += "INSERT INTO Words(`id`, `лемма`, `словоформа`, `часть речи`) VALUES (NULL, '{0}', '{1}', '{2}');\n".format(mystem.lemmatize(word)[0], word, 
                                                       get_speech_part(word, mystem))

print("---------------SQL запрос-------------------")
print(sql)
