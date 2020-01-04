from requests_html import HTMLSession
from threading import Thread, Lock

from concurrent.futures import ThreadPoolExecutor

from queue import Queue


locker = Lock()


def moz_parser(urls):
    while len(urls) > 0:

        with locker:
            url = urls.pop()

        try:

            with HTMLSession() as session:
                response = session.get(url)

        except Exception as e:
            print(type(e), e)
            with locker:
                urls.append(url)
            continue

        links = response.html.xpath('//h2/a')

        with locker:

            for link in links:

                href = link.attrs['href']
                name = link.text

                with open('results.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{href}\t{name}\n')

        print(f'SUCCESS | {url}')


def main():
    max_threads = 20

    base_url = 'https://moz.com/blog?page='
    all_pages = 385

    urls = []

    for i in range(2, all_pages + 1):
        url = base_url + str(i)
        urls.append(url)

    for t in range(max_threads):
        Thread(target=moz_parser, args=(urls, )).start()


if __name__ == '__main__':
    main()
