import requests
import json
import sys #чтобы была хорошая кодировка
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
import matplotlib.pyplot as plt
from datetime import datetime

application = 'https://api.vk.com/method/groups.getById?group_ids=dormitory8hse' #просто строка
response = requests.get (application) #надо переводить в json
data = json.loads (response.text) #помогаем джейсону сделать тхт
group_id = data ['response'][0]['gid'] #массив внутри словаря response, обращаемся к 1-ому элементу (0-ой порядковый номер), просим запомнить id

how_long = {}
output = open('text.txt', 'w', encoding='utf-8')
about_city = {}
about_age = {}

def user_information (user_id, length):
    users_inf = 'https://api.vk.com/method/users.get?user_ids=' + str (user_id) + '&fields=city,bdate'
    response = requests.get (users_inf)
    users_inf = json.loads (response.text)
    if user_id > 0:
        if 'city' in users_inf['response'][0]:
            cities = users_inf['response'][0]['city']
            if cities in about_city:
                about_city [cities].append (length)
            else:
                about_city [cities] = [length]
                
        if 'bdate' in users_inf['response'][0]:
            birth_user = users_inf['response'][0]['bdate'].split('.') #arr
            date_arr = str (datetime.today()).split()[0].split('-')
            if len (birth_user)>2:
                age = int (date_arr[0]) - int (birth_user[2])
                if age in about_age:
                    about_age [age].append (length)
                else:
                    about_age [age] = [length]            
                
offset = 1
for i in range (2):

    to_begin = 'https://api.vk.com/method/wall.get?owner_id=-'+ str (group_id) + '&count=100'+'&offset='+ str(100*i) 
    response_wall = requests.get (to_begin)
    data_wall = json.loads (response_wall.text) #плохая кодировка
    #for j in range (100):
    #    print (data_wall['response'][j+1]['text'].translate(non_bmp_map)) #в конце магия - перекодируем смайлики
    if i == 1:
        offset = 101
    for j in range (100):
        length = len(data_wall['response'][j+1]['text'].translate(non_bmp_map).split())
        #print(lenght)   
        print('Post N[', j+offset, ']', file = output)
        print(data_wall['response'][j+1]['text'].translate(non_bmp_map), file = output)
        post_id = data_wall['response'][j+1]['id']
        user_id = data_wall['response'][j+1]['from_id']
        user_information (user_id, length)
        comments_wall = 'https://api.vk.com/method/wall.getComments?owner_id=-'+ str (group_id) + '&post_id=' + str (post_id) + '&count=100'#+'&offset='+ str(100*i) 
        response_comments_wall = requests.get (comments_wall)
        data_comments_wall = json.loads (response_comments_wall.text)
        #print (data_comments_wall)
        print('Comments: ', file = output)
        for m in range (1,len (data_comments_wall['response'])):
            length_comment = len(data_comments_wall['response'][m]['text'].translate(non_bmp_map).split())
            print(data_comments_wall['response'][m]['text'].translate(non_bmp_map), file = output)
            user_id = data_comments_wall['response'][m]['uid'] #для поста - from_id, для коммента - uid
            user_information (user_id, length)
            #print (length_comment)
            if length in how_long:
                how_long [length].append (length_comment) #если такая длина уже есть, добавить значение
            else:
                how_long [length] = [length_comment]
#print (how_long)
output.close()

x_post = []
y_comment = []
for key in sorted(how_long):
    x_post.append(key)
    all_comments = 0
    for k in how_long[key]:
        all_comments+=k #суммируем длины комментов
    average = all_comments/len(how_long[key])
    y_comment.append(average)
print (x_post)
print (y_comment)
plt.plot(x_post,y_comment)
plt.show()

x_city = [] 
y_comment = []
for key in sorted(about_city):
    x_city.append(key)
    all_comments = 0
    for k in about_city[key]:
        all_comments+=k #суммируем длины комментов
    average = all_comments/len(about_city[key])
    y_comment.append(average)
print (x_city)
print (y_comment)
plt.plot(x_city,y_comment)
plt.show()

x_age = [] 
y_comment = []
for key in sorted(about_age):
    x_age.append(key)
    all_comments = 0
    for k in about_age[key]:
        all_comments+=k #суммируем длины комментов
    average = all_comments/len(about_age[key])
    y_comment.append(average)
print (x_age)
print (y_comment)
plt.plot(x_age,y_comment)
plt.show()      
    
#print (how_long)
#print (about_city)
#print (about_age)      
    

