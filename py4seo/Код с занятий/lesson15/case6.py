import random
from requests_html import HTMLSession
from threading import Lock

from concurrent.futures import ThreadPoolExecutor


locker = Lock()


URLS = []


def parser():
    while True:
        url = random.choice(URLS)
        try:
            with HTMLSession() as session:
                response = session.get(url, timeout=0.2)
                print(f'SUCCESS | {url}')
        except Exception as e:
            print(e, type(e))
        del url, response, session


def main():
    max_threads = 200

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for _ in range(max_threads):
            executor.submit(parser)


if __name__ == '__main__':
    main()
