from reppy.robots import Robots
from utils import *


domain = input('Enter domain: ')
proto = input('Enter http or https: ')

home_url = f'{proto}://{domain}/'
robots_url = home_url + 'robots.txt'

robots = Robots.fetch(robots_url)

filename = domain.replace('.', '_') + '.csv'
result_file = open(filename, 'w', encoding='utf-8')
result_file.write('URL\tTITLE\tH1\tRESPONSE_TIME\tLEVEL\n')

queue_urls = {home_url: 1}


def main():
    while len(queue_urls) > 0:

        min_level = min(queue_urls.values())

        for url, level in queue_urls.items():
            if level == min_level:
                queue_urls.pop(url)
                break

        print('Scan:', url, level)

        PARSED_URLS.add(url)

        title, h1, resp_time, links = url_parser(url)

        result = f'{url}\t{title}\t{h1}\t{resp_time}\t{level}\n'
        result_file.write(result)

        for link in links:
            if not link_filter(link, domain, robots):
                continue

            if link not in queue_urls:
                queue_urls[link] = level + 1


if __name__ == '__main__':
    main()
