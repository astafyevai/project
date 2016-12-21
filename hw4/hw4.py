import os, re

def my_stem ():
    path = 'C:' + os.sep + 'Users' + os.sep + 'irina' + os.sep + 'Desktop' + os.sep + 'hse' + os.sep + 'hw4' + os.sep + 'competition.txt'
    file = 'C:' + os.sep + 'Users' + os.sep + 'irina' + os.sep + 'Desktop' + os.sep + 'hse' + os.sep + 'hw4' + os.sep +'competition_mystem.txt'
    os.system ('C:\mystem.exe ' + path + ' ' + file + ' -nd')
    return file

def table_1 (file):
    
    file_txt = open ('competition_mystem.txt', 'r', encoding = 'utf-8')
    file_txt = file_txt.readlines ()
    file_sql = open ('competition_sql.sql', 'a', encoding = 'utf-8')
    file_sql.write ('CREATE TABLE Lemmas (id INTERGER PRIMARY KEY, wordform VARCHAR(100), lemma VARCHAR(100);\n')

    dicti = {}
    i = 0
    
    for line in file_txt:
        
        result = re.search ('(.*?){(.*?)}', 'file_txt')
        if result:
            wordform = result.group (1)
            if wordform not in dicti:
                dicti [wordform] = i
                lemma = result.group (2)
                file_sql.write ('INSERT INTO Lemmas (id, wordform, lemma) VALUES (' + str(i) + wordform + lemma + ');\n')
                i += 1
    return dicti

    file_sql.close ()


            
def table_2 (dicti):

    file_txt = open ('competition_mystem.txt', 'r', encoding = 'utf-8')
    file_txt = file_txt.readlines ()

    file_sql = open ('competition_sql.sql', 'a', encoding = 'utf-8')
    file_sql.write ('CREATE TABLE Uniq (id INTERGER PRIMARY KEY, wordform VARCHAR(100), number_lemma VARCHAR(100), number_wordform VARCHAR(100);\n')

    i = 0
    for word in file_txt:
        for key in dicti:
            if key == word:
                file_sql.write ('INSERT INTO Uniq (id, wordform, number_lemma, number_wordform) VALUES (' + str(i) + word + str (file_txt [key]) + ', ' + str (i + 1) + ');\n')
                i += 1
                
    file_sql.close ()
    return dicti
def main():
    table_2 (table_1 (my_stem ()))

if __name__ == '__main__':
    main()
    
