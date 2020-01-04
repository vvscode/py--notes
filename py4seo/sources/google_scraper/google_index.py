import pdb
import asyncio
import aiohttp
import aiosocks
import async_timeout
from lxml import html
from urllib.parse import quote
from aiosocks.connector import SocksConnector
# import uvloop
# asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


base_link = 'https://www.google.com/search?q={}'
# https://www.google.com.ua/search?q=info:https://www.elastic.co/guide/en/kibana/5.0/deb.html

treads = 50

proxy_key = '42d44afc61446caa32da5a1d6c1a6d1e'
proxy_url = "http://api.best-proxies.ru/proxylist.txt?key={}&limit={}&type=socks5&country=US".format(proxy_key, treads*10)


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "en-US;q=0.6,en;q=0.4",
    "Cache-Control": "max-age=0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"
}

regulars = {'sites': '//div[@class="rc"]'}


class Proxy:
    def __init__(self, host, port):
        self.host = str(host)
        self.port = int(port)


def get_data(code):
    tree = html.fromstring(code)
    result = dict()
    for element in regulars:
        result[element] = tree.xpath(regulars[element])
    if len(result['sites']):
        return True
    else:
        return False


async def worker(urls_q, proxies_q, proxies_q_good):
    while True:
        # Get proxy server from Queue and make proxy row string
        if not proxies_q_good.empty():
            proxy = await proxies_q_good.get()
        else:
            proxy = await proxies_q.get()

        if proxy is None:
            await asyncio.sleep(1)
            continue
        row = 'http://{host}:{port}'.format(host=proxy.host, port=proxy.port)

        # Get url from Queue

        if urls_q.empty():
            return
        else:
            page_url = await urls_q.get()

        url = base_link.format(quote('info:' + page_url))
        print(row, '-->', 'url', '| WPQ:', proxies_q_good.qsize(), '| APQ:', proxies_q.qsize())

        # Make http request with SOCKS proxy
        try:
            addr = aiosocks.Socks5Addr(proxy.host, proxy.port)
            conn = SocksConnector(proxy=addr)
            with async_timeout.timeout(30):
                async with aiohttp.ClientSession(connector=conn) as http_client:
                    async with http_client.get(url, headers=headers) as resp:
                        assert resp.status == 200
                        code = await resp.text()
            assert 'body' in code
        except Exception as e:
            print(type(e), e, '[worker, http_client.Exception]')
            await urls_q.put(page_url)
            continue

        # If proxy is working put it into good (working) proxies Queue again
        proxies_q_good.put_nowait(proxy)

        # Create dictionary data, to save it into database
        try:
            indexed = get_data(code)
            with open('data/google_index_result.txt', 'a', encoding='utf-8') as result:
                if indexed:
                    result.write('{}\t{}\n'.format(page_url, 'indexed'))
                else:
                    result.write('{}\t{}\n'.format(page_url, 'no'))
        except Exception as e:
            print(type(e), e, '[data_formatting Exception]')
            continue

        await asyncio.sleep(1)


async def crawler(urls_q, proxies_q, proxies_q_good):
    parser_jobs = [asyncio.ensure_future(worker(urls_q, proxies_q, proxies_q_good))for _ in range(treads)]
    await asyncio.gather(*parser_jobs)


async def add_urls_to_queue(urls_q):
    # file format
    # URL страницы
    # page_url

    with open('data/google_index_result.txt', 'r', encoding='utf-8') as result:
        result = result.read()

    with open('data/google_index_input.txt', 'r', encoding='utf-8') as f:
        for line in f:
            url = line.strip()
            if url not in result:
                await urls_q.put(url)


async def find_proxies(urls_q, proxies_q):
    while True:
        if urls_q.empty():
            return
        if proxies_q.qsize() < treads:
            print('Start finding proxies.')
            try:
                with async_timeout.timeout(30):
                    async with aiohttp.ClientSession() as client:
                        async with client.get(proxy_url) as resp:
                            code = await resp.text()
                proxies = [(x.split(':')[0], x.split(':')[1]) for x in code.split('\r\n')]
                proxies = list(set(proxies))
                print(proxies[:10], len(proxies))
            except Exception as e:
                print(type(e), e, '[Can not get proxies by API from source]')
                proxies = None

            try:
                for p in proxies:
                    proxies_q.put_nowait(Proxy(host=p[0], port=p[1]))
                print('Proxies Queue Size: ', proxies_q.qsize())
            except Exception as e:
                print(type(e), e, '[Exception in ProxyBroker]')
        await asyncio.sleep(5)


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()

        urls_q = asyncio.Queue()
        proxies_q = asyncio.Queue()
        proxies_q_good = asyncio.Queue()

        loop.run_until_complete(add_urls_to_queue(urls_q))
        task_crawler = asyncio.Task(crawler(urls_q, proxies_q, proxies_q_good))
        task_proxies = asyncio.Task(find_proxies(urls_q, proxies_q))

        loop.run_until_complete(asyncio.gather(task_crawler, task_proxies))
    except Exception as e:
        print(type(e), e, '[main Exception]')
