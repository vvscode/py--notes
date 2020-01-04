from requests_html import HTMLSession


class Website:
    __proto = 'HTTP'

    def __init__(self, url):
        self.url = url
        self.domain = url.split('/')[2]

    def print_something(self):
        print('AAAAAAAAAAAAAAA')
        print('This is Website!')

    def print_title(self):
        with HTMLSession() as session:
            self.response = session.get(self.url)
        print('TITLE: ', self.response.html.xpath('//title')[0].text)


class Shop(Website):
    def print_price(self):
        print('PRICE: ', 100500)

    def print_something(self):
        print('00000000000000000000')
        print('00000000000000000000')
        print('00000000000000000000')
        print('00000000000000000000')


class SearchEngine(Website):
    def position(self, keyword, domain):
        with HTMLSession() as session:
            resp = session.get(
                f'{self.url}/search?q={keyword}&num=100&hl=en')
        links = resp.html.xpath('//div[@class="r"]/a[1]/@href')
        for position, url in enumerate(links, start=1):
            if domain in url:
                print(f'Position for keyword: {keyword} ({domain}) is {position}')


py4you = Website('https://py4you.com/')

rozetka = Website('https://py4you.com/')

moyo = Shop('https://moyo.ua/')

google = SearchEngine('https://google.com.ua/')
