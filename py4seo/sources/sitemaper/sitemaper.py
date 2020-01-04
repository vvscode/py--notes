import pdb
import asyncio
import requests
import random
from lxml import html
from concurrent.futures import ThreadPoolExecutor
from time import time


base_sitemap = 'http://essaysforliterature.com/sitemap_single.xml'
result_file = 'urls_essaysforliterature.txt'

treads = 3

proxy_key = 'xxxx'
proxy_url = "http://api.best-proxies.ru/proxylist.txt?key={}&limit=0&type=http,https".format(proxy_key)


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US;q=0.6,en;q=0.4",
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
}


class Proxy:
    def __init__(self, host, port):
        self.host = str(host)
        self.port = int(port)
        self.row = '{host}:{port}'.format(host=host, port=port)

    def __str__(self):
        return '<Proxy {}>'.format(self.row)


def get_code(url, proxy=None):
    proxies = {'https': 'https://{}'.format(proxy.row), 'http': 'http://{}'.format(proxy.row)} if proxy else None
    print('GET from', proxy, '-->', url)
    resp = requests.get(url, headers=headers, timeout=180, proxies=proxies)
    assert resp.status_code == 200
    return resp.text


def get_links(code):
    if 'sitemapindex' in code:
        _type = 'sitemapindex'
        urls = html.fromstring(code.encode('utf-8')).xpath('//sitemap/loc/text()')
    else:
        _type = 'urls'
        urls = html.fromstring(code.encode('utf-8')).xpath('//url/loc/text()')
    return _type, urls


async def worker(urls_q, proxies_q, proxies_q_good, loop, executor):
    while urls_q.qsize():
        # Get proxy server from Queue and make proxy row string
        if not proxies_q_good.empty():
            proxy = await proxies_q_good.get()
        else:
            if not proxies_q.empty():
                proxy = await proxies_q.get()
            else:
                await asyncio.sleep(2)
                continue

        # Get link
        map_link = await urls_q.get()

        # Make http request with proxy
        try:
            t = time()
            code = await loop.run_in_executor(executor, get_code, map_link)
            print(time() - t, 'Response time')
            assert type(code) is str and len(code) > 100
        except Exception as e3:
            print(type(e3), e3, '[worker, code.Exception]', map_link)
            urls_q.put_nowait(map_link)
            continue

        # If proxy is working put it into good (working) proxies Queue again
        proxies_q_good.put_nowait(proxy)

        # Create dictionary data, to save it into database
        try:
            t1 = time()
            data = get_links(code)
            print(time() - t1, 'Getlinks time')
            if data[0] == 'sitemapindex':
                for u in data[1]:
                    urls_q.put_nowait(u)
            else:
                t2 = time()
                with open(result_file, 'a', encoding='utf-8') as file:
                    for u in data[1]:
                        file.write(u+'\n')
                print(time() - t2, 'File writing')
            print('[OK]', proxy.row, '-->', map_link,
                  '| WPQ:', proxies_q_good.qsize(), '| APQ:', proxies_q.qsize(), '| URLsQ:', urls_q.qsize())
        except Exception as e4:
            print(type(e4), e4, '[data_formatting Exception]', map_link)


def first(urls_q):
    print('GET', '-->', base_sitemap)
    code = get_code(base_sitemap)
    try:
        data = get_links(code)
        if data[0] == 'sitemapindex':
            for u in data[1]:
                urls_q.put_nowait(u)
            print('Find', urls_q.qsize(), 'sitemaps')
        else:
            with open(result_file, 'a', encoding='utf-8') as f:
                for u in data[1]:
                    f.write(u + '\n')
            print('Done!', len(data[1]), 'urls')
    except Exception as e:
        print(type(e), e)


async def find_proxies(urls_q, proxies_q, loop, executor):
    while urls_q.qsize():
        if proxies_q.qsize() < treads:
            print('Start finding proxies.')
            try:
                code = await loop.run_in_executor(executor, get_code, proxy_url)
                proxies = [(x.split(':')[0], x.split(':')[1]) for x in code.split('\r\n') if x]
                random.shuffle(proxies)
                print(proxies[:10], len(proxies))
            except Exception as e1:
                print(type(e1), e1, '[Can not get proxies by API from source]')
                proxies = []
            try:
                for p in proxies:
                    proxies_q.put_nowait(Proxy(host=p[0], port=p[1]))
                print('Proxies Queue Size: ', proxies_q.qsize())
            except Exception as e2:
                print(type(e2), e2, '[Exception in ProxyBroker]')
        await asyncio.sleep(5)


async def crawler(urls_q, proxies_q, proxies_q_good, loop, executor):
    jobs = [worker(urls_q, proxies_q, proxies_q_good, loop, executor) for _ in range(treads)]
    await asyncio.gather(*jobs)


def main():
    loop = asyncio.get_event_loop()
    executor = ThreadPoolExecutor(max_workers=treads)

    urls_q = asyncio.Queue()
    first(urls_q)

    proxies_q = asyncio.Queue()
    proxies_q_good = asyncio.Queue()

    loop.create_task(find_proxies(urls_q, proxies_q, loop, executor))
    loop.create_task(crawler(urls_q, proxies_q, proxies_q_good, loop, executor))

    loop.run_forever()


if __name__ == '__main__':
    main()
