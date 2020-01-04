from requests_html import HTMLSession
from threading import Lock

from concurrent.futures import ThreadPoolExecutor


locker = Lock()


def moz_parser(url):
    with HTMLSession() as session:
        response = session.get(url)
    links = response.html.xpath('//h2/a')
    with locker:
        for link in links:
            href = link.attrs['href']
            name = link.text
            with open('results.txt', 'a', encoding='utf-8') as f:
                f.write(f'{href}\t{name}\n')
    print(f'SUCCESS | {url}')


def urls_gen(num):
    base_url = 'https://moz.com/blog?page='
    for i in range(2, num + 1):
        yield base_url + str(i)


def main():
    max_threads = 20
    urls = urls_gen(385)

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(moz_parser, urls)


if __name__ == '__main__':
    main()
