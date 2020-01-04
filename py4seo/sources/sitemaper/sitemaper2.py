import pdb
import requests
import random
from lxml import html
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from time import sleep


base_sitemap = 'https://www.olx.ua/sitemap_single.xml'
result_file = 'urls_olx.txt'

treads = 200

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
    # print('GET from', proxy, '-->', url)
    resp = requests.get(url, headers=headers, timeout=600, proxies=proxies)
    assert resp.status_code == 200
    return resp.content


def get_links(code):
    if b'sitemapindex' in code:
        _type = 'sitemapindex'
        urls = html.fromstring(code).xpath('//sitemap/loc/text()')
    else:
        _type = 'urls'
        urls = html.fromstring(code).xpath('//url/loc/text()')
    return _type, urls


def worker(urls_q, proxies_q, proxies_q_good):
    while urls_q.qsize():
        # Get proxy server from Queue and make proxy row string
        if not proxies_q_good.empty():
            proxy = proxies_q_good.get()
        else:
            if not proxies_q.empty():
                proxy = proxies_q.get()
            else:
                sleep(2)
                continue

        # Get link
        map_link = urls_q.get()

        # Make http request with proxy
        try:
            content = get_code(map_link, proxy)
            assert b'sitemaps.org' in content
        except Exception:
            # print(type(e3), e3, '[worker, code.Exception]', map_link)
            urls_q.put(map_link)
            continue

        # If proxy is working put it into good (working) proxies Queue again
        proxies_q_good.put_nowait(proxy)

        # Create dictionary data, to save it into database
        try:
            data = get_links(content)
            if data[0] == 'sitemapindex':
                for u in data[1]:
                    urls_q.put_nowait(u)
            else:
                with open(result_file, 'a', encoding='utf-8') as file:
                    for u in data[1]:
                        file.write(u+'\n')
            print('[OK]', proxy.row, '-->', map_link,
                  '| WPQ:', proxies_q_good.qsize(), '| APQ:', proxies_q.qsize(), '| URLsQ:', urls_q.qsize())
        except Exception as e4:
            print(type(e4), e4, '[data_formatting Exception]', map_link)


def first(urls_q):
    content = get_code(base_sitemap)
    try:
        data = get_links(content)
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


def find_proxies(urls_q, proxies_q):
    while urls_q.qsize():
        if proxies_q.qsize() < treads:
            print('Start finding proxies.')
            try:
                code = get_code(proxy_url).decode('utf-8')
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
        sleep(5)


def main():
    urls_q = Queue()
    first(urls_q)
    proxies_q = Queue()
    proxies_q_good = Queue()

    with ThreadPoolExecutor(max_workers=treads+1) as executor:
        executor.submit(find_proxies, urls_q, proxies_q)
        for i in range(treads):
            executor.submit(worker, urls_q, proxies_q, proxies_q_good)


if __name__ == '__main__':
    main()
