import random
from requests_html import HTMLSession
from datetime import date
from time import time, sleep

domain = 'py4you.com'
t1 = time()
count = 0

parsed_date = date.today().isoformat()

# Взял из файла все ключи
with open('keys.txt', 'r', encoding='utf-8') as f1:
    keywords = {line.strip() for line in f1}

# Взял из файла все УЖЕ ОТСКАНИРОВАННЫЕ ключи
with open('keys_parsed.txt', 'r', encoding='utf-8') as f2:
    keywords_parsed = {line.strip() for line in f2}

# Цикл по ключам все минус отсканированные
for key in (keywords - keywords_parsed):

    print(f'Send request for key: [{key}]')

    sleep(random.randint(1, 5))

    with HTMLSession() as session:
        try:

            resp = session.get(
                f'https://www.google.com/search?q={key}&num=100&hl=en')

            if resp.status_code != 200:
                raise ValueError('Status code is not 200')

            links = resp.html.xpath('//div[@class="r"]/a[1]/@href')
            found = 'not_found'

            with open('keys_parsed.txt', 'a', encoding='utf-8') as f3:
                f3.write(key + '\n')

        except Exception as e:
            print(type(e), e)
            links = []
            found = 'ban_google'

    position = 1
    for url in links:
        if domain in url:
            found = 'found'
            result = f'{parsed_date}\t{key}\t{url}\t{position}\n'
            with open('results.csv', 'a', encoding='utf-8') as f2:
                f2.write(result)
        position = position + 1

    if found != 'found':
        with open('results.csv', 'a', encoding='utf-8') as f2:
            result = f'{parsed_date}\t{key}\t{found}\t-\n'
            f2.write(result)


t2 = time()
print(f'All done!')
print('Working time is: ', round(t2-t1, 4), ' seconds')
