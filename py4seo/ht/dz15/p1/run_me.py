# From `case-2.py` (https://drive.google.com/drive/u/0/folders/1UvubgSa5s827kQhIRKvg8o-SVBdvWTZ_)
from requests_html import HTMLSession
from threading import Thread, Lock

from concurrent.futures import ThreadPoolExecutor

from queue import Queue

import db


locker = Lock()


def moz_parser(q):
    while q.qsize() > 0:
        url = q.get()
        try:

            with HTMLSession() as session:
                response = session.get(url)

        except Exception as e:
            print(type(e), e)
            q.put(url)
            continue

        links = response.html.xpath('//h2/a')

        with locker:
            db.LinkRecord.insert_many(
                map(
                    lambda link: {
                        "url": link.attrs["href"],
                        "name": link.text,
                        "page_url": url,
                    },
                    links,
                )
            ).execute()

        print(f'SUCCESS | {url}')


def main():
    max_threads = 20

    base_url = 'https://moz.com/blog?page='
    all_pages = 385

    urls_queue = Queue()

    for i in range(2, all_pages + 1):
        url = base_url + str(i)
        urls_queue.put(url)

    for t in range(max_threads):
        Thread(target=moz_parser, args=(urls_queue, )).start()


if __name__ == '__main__':
    main()