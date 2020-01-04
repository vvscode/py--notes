import os
import json
import requests
from pprint import pprint
from requests_html import HTMLSession
from bs4 import BeautifulSoup

api_url = 'http://api.text.ru/post'
api_key = '149528e60a44395ac4792d550d47061b'
exceptdomain = 'parkinson.su, karkasniy-dom.com'
stage = str(input('Input the step of getting data(1 - send request or 2 - get result): \n'))

# path = input ('Input path to the file with text to check: ')
# exceptdomain = input ('Input domain to except: ')

if stage == '1':

    with open('D://Temp//data.txt', 'r', encoding='utf-8') as myfile:
        data = myfile.read()

    post_data = {
        'text': data,
        'userkey': api_key,
        'exceptdomain': exceptdomain
    }

    print(f'Sending text to <<Text.Ru>> to check plague with the following parameters:\n {post_data}')

    with HTMLSession() as session:
        response = session.post(api_url, data=post_data)

    data = response.json()
    with open('D://Temp//text_uid.txt', 'w', encoding='utf-8') as myfile:
        myfile.write(data['text_uid'])

elif stage == '2':
    with open('D://Temp//text_uid.txt', 'r', encoding='utf-8') as myfile:
        text_uid = myfile.read()

    post_data = {
        'uid': text_uid,
        'userkey': api_key,
        'jsonvisible': 'detail'
    }

    print(f'Sending query to get the result from <<Text.Ru>> with following parameters:\n {post_data}\n')
    response = requests.post(api_url, data=post_data)
    # with HTMLSession() as session:
    #    response = session.post(api_url, data=post_data)
    response.encoding = 'utf-8-sig'

    data = response.json()

else:
    print('Wrong choice')
result = data['result_json']

print(f'Result:\n {result}')
