import urllib.request, re, html

def openning ():
    links = []
    f = open ('links.txt', 'r')
    for line in f:
        links.append(line)
    f.close()
    return links

def text (links):
    regs = ['<div class="descr">.*?<p>(.+?)</p> </div>',
            '<!--dle_image_end--></div><br /><br />(.+?).*?</div>',
            '<div class="maincont" itemprop="articleBody">(.+?)<div class="author">',
            '<div itemprop="articleBody" style="display: none"><p>(.+?)<div itemprop="dateCreated" style="display: none">'
            ]

    texts = []
    for i in links:
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        req = urllib.request.Request(i, headers={'User-Agent':user_agent})
        with urllib.request.urlopen(req) as response:
            html_page = response.read().decode('windows-1251')
            for j in regs:
                regLink = re.compile (j, flags=re.U | re.DOTALL)
                text = regLink.search(html_page)
                if text:
                    new = text.group(1)
                    regTag = re.compile ('<.*?>', flags = re.U | re.DOTALL)
                    regTab = re.compile ('\t', flags = re.U | re.DOTALL)
                    regStr = re.compile ('\n', flags = re.U | re.DOTALL)
                    new = regTag.sub ('', html.unescape(new))
                    new = regTab.sub (' ', new)
                    regStr.sub (' ', new)
                    texts.append (new)
    return texts


def words (texts):
    devide_texts = []
    for text in texts:
        words = text.split ()
        for indx, word in enumerate (words):
            words [indx] = word.strip(' ,:;«».!?')
            if words [indx] == '' or words [indx] == '–':
                words.remove (words[indx])
        devide_texts.append (words)
    return devide_texts

def words_2 (devide_texts):
    
    devide_texts_set = []
    for words in devide_texts:
        devide_texts_set.append(set(words))
    return devide_texts_set


def common (devide_texts_set):
    file_1 = open ('common_words.txt', 'w')
    common = devide_texts_set[0] & devide_texts_set[1] & devide_texts_set[2] & devide_texts_set[3]
    for i in sorted (common):
        file_1.write (i + '\n')
    file_1.close()


def count_frequency (devide_texts_set):
    frequency = {}
    for devide_texts in devide_texts_set:
        for words in devide_texts:
            if words in frequency:
                frequency [words] += 1
            else:
                frequency [words] = 1
    return frequency


def uniq_words (devide_texts_set, frequency):
    file_2 = open('unique_words.txt', 'w')
    unique = devide_texts_set[0] ^ devide_texts_set[1] ^ devide_texts_set[2] ^ devide_texts_set[3]
    for i in sorted (unique):
        if frequency [i] > 1:
            file_2.write (i + '\n')
    file_2.close()


def main ():
    devide_texts_set = (words_2(words (text (openning ()))))
    common (devide_texts_set)
    uniq_words (devide_texts_set, count_frequency (devide_texts_set))

if __name__ == '__main__':
    main()
