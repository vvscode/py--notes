from time import sleep
from random import randint
from requests_html import HTMLSession

print('Start working')

with open('keywords.txt', 'r') as f:
    keywords = [line.strip() for line in f]

print(f'We need to parse {len(keywords)} keywords')

session = HTMLSession()

result_file = open('results.csv', 'a')

for key in keywords:
    google_url = f'https://www.google.com/search?q={key}&num=100&hl=en'
    print('SEND REQUEST TO GOOGLE: ', key)
    resp = session.get(google_url)
    links = resp.html.xpath('//h3/a/@href')
    print(f'Found {len(links)} links.')
    for position, link in enumerate(links, 1):
        if not link.startswith('http'):
            continue
        domain = link.split('/')[2]
        result_file.write(f'{key}\t{link}\t{domain}\t{position}\n')
    random_timeout = randint(5, 10)
    print(f'Sleep {random_timeout} seconds')
    sleep(random_timeout)

result_file.close()

print('All Done!')
