from pymorphy2 import MorphAnalyzer
import random
import telebot
import conf
import flask

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
app = flask.Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Давай поиграем!')

@bot.message_handler(func=lambda m: True) # здесь описываем, на какие сообщения реагирует функция

def my_function(message): 
    # здесь код, который генерирует ответ
    def find_POS(POS, arr):
        temp = arr[POS]    
        idx = random.randint(0, len(temp) - 1)
        return temp[idx]

    def examine(word, arr):
        obj = morph.parse(word)[0]
        POS = obj.tag.POS
        word_to_print = find_POS(POS, arr)
        i = str(obj.tag).find(',')
        r = str(obj.tag).find(' ')
        string = str(obj.tag)[i+1:]
        string = string.replace(" ",",")

        if r != -1:
            tag = frozenset(string.split(','))
        else:
            tag = frozenset()
        return tag, word_to_print
 
    morph = MorphAnalyzer()

    text = str(message.text)
    reply = str()
    
    if not text.isalnum() and ' ' not in text:
        reply = 'Введены непонятные символы :('
    else:
        words_separated = text.split()

        file_str = open('1grams-3.txt', 'r', encoding='utf-8').read()

        words_separated_new = file_str.split()

        arr = dict()
        idx = 0

        for word in words_separated_new:
            idx += 1
            temp = morph.parse(word)[0]
            if temp.tag.POS in arr:
                arr[temp.tag.POS].append(temp.normal_form)
            else:
                arr[temp.tag.POS] = [temp.normal_form]
            if idx == 10000:
                break
            
        info = None

        for word in words_separated:
            info = None
            while info == None:
                tag, word_to_print = examine(word, arr)
                info = morph.parse(word_to_print)[0].inflect(tag)   
            reply += info.word + ' '
        
    bot.send_message(message.chat.id, reply)  # отправляем в чат ответ
	
if __name__ == '__main__':
    bot.polling(none_stop=True)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'
