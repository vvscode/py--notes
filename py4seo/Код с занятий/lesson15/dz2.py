from requests_html import HTMLSession
from threading import Thread, Lock

from concurrent.futures import ThreadPoolExecutor

from queue import Queue


locker = Lock()


def moz_parser(q):

    while q.qsize() > 0:

        url = q.get()

        # b = 100 / 0
        #
        # print(b)

        try:

            with HTMLSession() as session:
                response = session.get(url)

        except Exception as e:
            print(type(e), e)
            q.put(url)
            continue

        links = response.html.xpath('//h2/a')

        with locker:

            for link in links:

                href = link.attrs['href']
                name = link.text

                with open('results.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{href}\t{name}\n')

        print(f'SUCCESS | {url}')


def moz_parser2(url):
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


def main():
    max_threads = 20

    base_url = 'https://moz.com/blog?page='
    all_pages = 385

    urls_queue = Queue()

    urls = []

    for i in range(2, all_pages + 1):
        url = base_url + str(i)
        urls_queue.put(url)
        urls.append(url)

    # for t in range(10):
    #     Thread(target=moz_parser, args=(urls_queue, )).start()

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # for _ in range(max_threads):
        #     executor.submit(moz_parser, urls_queue)
        executor.map(moz_parser2, urls)


if __name__ == '__main__':
    main()
