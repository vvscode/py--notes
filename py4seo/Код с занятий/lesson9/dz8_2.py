from time import time
from requests_html import HTMLSession
from reppy.robots import Robots


class Parser:

    def __init__(self, domain, schema):
        self.domain = domain
        self.schema = schema

        self.home_url = f'{self.schema}://{self.domain}/'
        self.robots_url = self.home_url + 'robots.txt'

        self.robots = Robots.fetch(self.robots_url)

        self.filename = domain.replace('.', '_') + '.csv'
        self.result_file = open(self.filename, 'w', encoding='utf-8')
        self.result_file.write('URL\tTITLE\tH1\tRESPONSE_TIME\tLEVEL\n')

        self.queue_urls = {self.home_url: 1}

        self.PARSED_URLS = set()

    def url_parser(self, url):
        with HTMLSession() as session:
            t1 = time()
            response = session.get(url, proxies={})
            t2 = time()
        try:
            title = response.html.xpath('//title')[0].text
        except Exception as e:
            title = 'not_found'
        try:
            h1 = response.html.xpath('//h1')[0].text
        except Exception as e:
            h1 = 'not_found'
        resp_time = round(t2 - t1, 2)
        links = response.html.absolute_links

        return title, h1, resp_time, links

    def link_filter(self, link):
        if '#' in link:
            link = link.split('#')[0]
        if link.endswith('.jpg'):
            return False
        if self.domain not in link:
            return False
        if link in self.PARSED_URLS:
            return False
        if not self.robots.allowed(link, '*'):
            return False
        return True

    def main(self):
        while len(self.queue_urls) > 0:

            min_level = min(self.queue_urls.values())

            for url, level in self.queue_urls.items():
                if level == min_level:
                    self.queue_urls.pop(url)
                    break

            print('Scan:', url, level)

            self.PARSED_URLS.add(url)

            title, h1, resp_time, links = self.url_parser(url)

            result = f'{url}\t{title}\t{h1}\t{resp_time}\t{level}\n'
            self.result_file.write(result)

            for link in links:
                if not self.link_filter(link):
                    continue

                if link not in self.queue_urls:
                    self.queue_urls[link] = level + 1


if __name__ == '__main__':
    domain = input('Enter domain: ')
    proto = input('Enter http or https: ')

    pr = Parser(domain, proto)
    pr.main()
