import re, os, html, json
from flask import Flask, render_template, request

app = Flask (__name__)

def thai_english ():
    arr = []
    dic = {}
    regex = re.compile ("<tr><td class=th><a href='/id/.+?'>(.+?)</a></td><td>.+?</td><td>(.+?)</td></tr>", re.DOTALL) #достаю слова, потом чищу
    regTag = re.compile ('<.*?>', re.DOTALL)
    reg1 = re.compile ('\xa0', re.DOTALL)
    
    for root, dirs, files in os.walk ('.\\thai_pages'):
        for i in files:
            file_read = open (root + os.sep + i, 'r', encoding = 'utf-8') #читаю файл, чищу
            whole_text = file_read.read ()
            all_words = regex.findall (whole_text)
            for words in all_words:
                for word in words:
                    word_without_symb = regTag.sub ('', word)
                    word_without_symb = reg1.sub ('', word_without_symb)
                    arr.append(word_without_symb)
                    
    for i in range (0, len (arr), 2):
        arr [i] = html.unescape (arr[i]) #добавляю в массив слова через одно: слово-перевод, записываю в словарь, возвращаю словарь
        arr [i+1] = html.unescape (arr[i+1])
        dic [arr[i]] = arr [i+1]


    thai_eng = open ('thai_eng.json', 'w', encoding = 'utf-8') #записываю всё в json
    strr = json.dumps (dic, ensure_ascii = False)
    thai_eng.write (strr)
    thai_eng.close ()

    return dic

def english_thai (dic):
    eng_thai_dic = {}
    for i in dic:
        if dic [i] not in eng_thai_dic:
            eng_thai_dic [dic[i]] = [i] #если нет перевода - присвоить i
        else:
            eng_thai_dic [dic[i]].append(i) #если есть перевод - добавить
            
    eng_thai = open ('eng_thai.json', 'w', encoding = 'utf-8')
    strr = json.dumps (eng_thai_dic, ensure_ascii = False)
    eng_thai.write(strr)
    eng_thai.close()


def main():
    thai_english ()
    english_thai(thai_english())
    
if __name__ == '__main__':
    main ()
    app.run(debug = True)


