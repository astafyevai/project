import json
from flask import Flask
from flask import url_for, render_template, request, redirect
from urllib.parse import unquote

app = Flask(__name__)

@app.route ('/')
def index ():
    if request.args:
        name = unquote(request.args['username'])
        answer = unquote(request.args['answer'])
        age = unquote(request.args['age'])
        language = unquote(request.args['language'])
        motherland = unquote(request.args['motherland'])
        nowdays = unquote(request.args['nowdays'])
        arm = unquote(request.args['arm'])
        hand = unquote(request.args['hand'])
        neck = unquote(request.args['neck'])
        head = unquote(request.args['head'])
        face = unquote(request.args['face'])
        leg = unquote(request.args['leg'])
        foot = unquote(request.args['foot'])


        arr = [name, answer, age, language, motherland, nowdays, arm, hand, neck, head, face, leg, foot]
        saving_json (arr)
        saving_txt (arr)
    return render_template ('index.html')

def saving_json (arr):
    results = open ('data.json', 'a', encoding = 'utf-8')
    s = json.dumps (arr)
    results.write (s + '\n')
    results.close ()

def saving_txt (arr):
    results = open ('data.txt', 'a', encoding = 'utf-8')
    s = ''
    for i in arr:
        if s == '':
            s = i
        else:
            s = s + '\t' + i
        
    results.write (s + '\n')
    results.close ()
    
def get_arr ():
    statistic = open ('data.txt', 'r', encoding = 'utf-8')
    text = statistic.readlines ()
    feedback = []
    for i in text:
        one_answer = i.split () #деление на ячейки
        feedback.append (one_answer) #массив из словарей
    return feedback
    
@app.route ('/stats')
def stat ():
    feedback = get_arr ()
    return render_template ('statistic.html', answer = feedback)

@app.route('/json')
def jsn ():
    json1 = open ('data.json', 'r')
    jsn = json1.read ()
    json1.close ()
    return render_template ('json.html', jsn = jsn)


@app.route('/search')
def searching ():
    return render_template ('search.html')

@app.route('/results')
def result ():
    if request.args:
        language = unquote(request.args['language'])
        motherland = unquote(request.args['motherland'])
        nowdays = unquote(request.args['nowdays'])
    
    feedback = []
    arr = get_arr ()
    for ans in arr:
        if language == ans [3] or motherland == ans[4] or nowdays == ans [5]:
            feedback.append (ans)
    return render_template ('results.html', answer = feedback)
    

if __name__ == '__main__':
    app.run(debug = True)
