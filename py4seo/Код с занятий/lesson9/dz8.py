from time import time
from requests_html import HTMLSession
from reppy.robots import Robots


domain = input('Enter domain: ')
proto = input('Enter http or https: ')

home_url = f'{proto}://{domain}/'
robots_url = home_url + 'robots.txt'

robots = Robots.fetch(robots_url)

filename = domain.replace('.', '_') + '.csv'
result_file = open(filename, 'w', encoding='utf-8')
result_file.write('URL\tTITLE\tH1\tRESPONSE_TIME\tLEVEL\n')

queue_urls = {home_url: 1}

PARSED_URLS = set()


class Parser:

    @staticmethod
    def url_parser(url):
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

    @staticmethod
    def link_filter(link, domain, robots):
        if '#' in link:
            link = link.split('#')[0]
        if link.endswith('.jpg'):
            return False
        if domain not in link:
            return False
        if link in PARSED_URLS:
            return False
        if not robots.allowed(link, '*'):
            return False
        return True

    @staticmethod
    def main():
        while len(queue_urls) > 0:

            min_level = min(queue_urls.values())

            for url, level in queue_urls.items():
                if level == min_level:
                    queue_urls.pop(url)
                    break

            print('Scan:', url, level)

            PARSED_URLS.add(url)

            title, h1, resp_time, links = Parser.url_parser(url)

            result = f'{url}\t{title}\t{h1}\t{resp_time}\t{level}\n'
            result_file.write(result)

            for link in links:
                if not Parser.link_filter(link, domain, robots):
                    continue

                if link not in queue_urls:
                    queue_urls[link] = level + 1


if __name__ == '__main__':
    pr = Parser()
    pr.main()
