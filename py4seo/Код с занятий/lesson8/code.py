from PIL import Image
from requests_html import HTMLSession


class LogoImage:
    def __init__(self, file):
        self.file = file
        self.img = Image.open(file)

    def show_image(self):
        self.img.show()


class SEO:

    def __init__(self, links_count, keywords_count,
                 traffic, domains_count, title_duplicates):
        self.links_count = links_count
        self.keywords_count = keywords_count
        self.traffic = traffic
        self.domains_count = domains_count
        self.title_duplicates = title_duplicates

    def show_website_seo(self):
        print('links_count:', self.links_count)
        print('keywords_count:', self.keywords_count)
        print('traffic:', self.traffic)
        print('domains_count:', self.domains_count)
        print('title_duplicates:', self.title_duplicates)


class Website:
    aaa = 'bbb'
    __proto = 'HTTP'

    def __init__(self, url):
        # super().__init__(123, 345, 4356, 567, 78)
        self.url = url
        self.domain = self.url.split('/')[2]

    def print_something(self):
        print('AAAAAAAAAAAAAAA')
        print('This is Website!')

    def print_title(self):
        with HTMLSession() as session:
            self.response = session.get(self.url)
        print('TITLE: ', self.response.html.xpath('//title')[0].text)


class Shop(Website):

    def __init__(self, sale, min_price, products_count, url, logo):

        super(Shop, self).__init__(url)
        # super(Website, self).__init__(10, 324, 345, 546, 67)

        self.sale = sale
        self.min_price = min_price
        self.products_count = products_count
        self.logo = LogoImage(logo)

    def print_price(self):
        print('PRICE: ', 100500)

    def print_something(self):
        print('00000000000000000000')
        print('00000000000000000000')
        print('00000000000000000000')
        print('00000000000000000000')


moyo = Shop(10, 1, 123123213, 'https://moyo.ua/', 'logo.png')

moyo.print_title()
