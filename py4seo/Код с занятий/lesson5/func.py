import random
from requests_html import HTMLSession
from datetime import date
from time import time, sleep


t1 = time()


parsed_date = 1000


def serp_parser(key, domain='py4you.com', a=100, b=1000):

    global parsed_date

    parsed_date = parsed_date + 10010

    print('Send request:', key)

    with HTMLSession() as session:
        try:
            resp = session.get(
                f'https://www.google.com/search?q={key}&num=100&hl=en')
            if resp.status_code != 200:
                raise ValueError('Status code is not 200')
            links = resp.html.xpath('//div[@class="r"]/a[1]/@href')
            found = 'not_found'
        except Exception as e:
            print(type(e), e)
            links = []
            found = 'ban_google'

    result = [parsed_date, key, found, '-']

    for position, url in enumerate(links, 1):
        if domain in url:
            result = [parsed_date, key, url, position]

    return result, 'blabla', 'data', 'url'


t2 = time()


my_position1 = serp_parser('python for seo')
my_position2 = serp_parser('python for you')
my_position3 = serp_parser('заказать seo')


# data = ('купить seo', 'rozetka.com.ua', 1001)

data = {
    'key': 'купить seo',
    'domain': 'rozetka.com.ua',
    'a': 1000
}


# my_position4 = serp_parser(data[0], data[1], data[2], data[3])

my_position4 = serp_parser(**data)

print(f'All done!')

print(my_position1)
print(my_position2)
print(my_position3)
print(my_position4)

print('Working time is: ', round(t2-t1, 4), ' seconds')

print(parsed_date)
