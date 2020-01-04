import random
from requests_html import HTMLSession
from googletrans import Translator


def parser(key):

    with HTMLSession() as session:
        headers = {'User-Agent': get_random_agent()}
        print(headers)
        resp = session.get(f'https://www.google.com.ua/search?q={key}&num=100&hl=ru', headers=headers)
        print(resp)
        links = resp.html.xpath('//div[@class="r"]/a[1]/@href')[:3]
        print(links)

        for url in links:
            print(url)
            with HTMLSession() as session:
                response = session.get(url)
                print(f'Тянем сайт с: {url}')
            try:
                orig = response.html.xpath('//p')[0].text
            except Exception as e:
                orig = 'no text'
            print(f'Оригинал: {orig}')

        translator = Translator()
        content = translator.translate(orig)

        print(f'Перевод: {content}')
        return content


def get_random_agent():
        with open('UA.txt') as f:
            agents = [x.strip() for x in f]
        return random.choice(agents)

# def translation():
#     trans = Translator()
#     trans.translate()
#     return trans


# def translate():
#     translator = Translator()
#     translator.translate(origin, src='ru')
#     content = translator.text
#     print(f'Пеервод: {content}')
#     return content




texts = parser('какие бывают очки')


# print(texts)
# translator.translate('veritas lux mea', src='la').text
