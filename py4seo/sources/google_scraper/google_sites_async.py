import pdb
import asyncio
import aiohttp
from lxml import html
from urllib.parse import quote, unquote
from aiosocks.connector import ProxyConnector, ProxyClientRequest
from pirat import headers, find_proxies_async
from yarl import URL


base_link = 'https://www.google.com/search?q={}&num=100'
# base_link = 'https://www.bing.com/search?q={}&count=50'
# base_link = 'https://search.yahoo.com/search?n=100&p={}'

treads = 100

regulars = {'sites': '//h3/a/@href'}

input_file = 'data/google_sites_input_Andrey.txt'
result_file = 'data/google_sites_result_Andrey2.txt'


def get_sites(code, keyword):
    tree = html.fromstring(code)
    result, sites = {}, []
    for element in regulars:
        result[element] = tree.xpath(regulars[element])
    if len(result['sites']) == 0:
        sites.append((keyword, 'n/f', 'n/f'))
        return sites
    for n, url in enumerate(result['sites'], start=1):
        try:
            url = unquote(url[url.index('RU=')+3:url.index('/RK=1')])
            sites.append((keyword, url, n))
        except:
            pass
    return sites


async def worker(urls_q, proxies_q, proxies_q_good):
    while urls_q.qsize():
        # Get proxy from Queue
        if not proxies_q_good.empty():
            proxy = await proxies_q_good.get()
        else:
            if not proxies_q.empty():
                proxy = await proxies_q.get()
            else:
                await asyncio.sleep(1)
                continue
        # Get data from Queue
        key = await urls_q.get()

        url = base_link.format(quote(key))
        print(proxy.row, '-->', 'url', '| WPQ:', proxies_q_good.qsize(), '| APQ:', proxies_q.qsize())

        # Make http request with SOCKS proxy
        try:
            async with aiohttp.ClientSession(connector=ProxyConnector(), request_class=ProxyClientRequest,
                                             conn_timeout=120) as http_client:
                async with http_client.get(url, headers=headers, proxy=proxy.socks5) as resp:
                    assert resp.status == 200
                    code = await resp.text()
            assert 'body' in code
        except Exception as e:
            print(type(e), e, '[worker, http_client.Exception]')
            await urls_q.put(key)
            continue

        # If proxy is working put it into good (working) proxies Queue again
        proxies_q_good.put_nowait(proxy)

        # Create dictionary data, to save it into database
        try:
            sites = get_sites(code, key)
            if sites:
                with open(result_file, 'a', encoding='utf-8') as result:
                    for site in sites:
                        result.write('{}\t{}\t{}\n'.format(*site))
                        # result.write('{}\n'.format(URL(site[1]).host))
        except Exception as e:
            print(type(e), e, '[data_formatting Exception]')
            continue


async def crawler(urls_q, proxies_q, proxies_q_good):
    parser_jobs = [asyncio.ensure_future(worker(urls_q, proxies_q, proxies_q_good))for _ in range(treads)]
    await asyncio.gather(*parser_jobs)


async def add_urls_to_queue(urls_q):
    with open(result_file, 'r', encoding='utf-8') as result:
        result = [x.strip() for x in result.read().split('\n')]
        result = set([x.split('\t')[0].strip() for x in result])
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            keyword = line.strip()
            if keyword not in result:
                await urls_q.put(keyword)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    urls_q = asyncio.Queue()
    proxies_q = asyncio.Queue()
    proxies_q_good = asyncio.Queue()
    loop.run_until_complete(add_urls_to_queue(urls_q))
    task_crawler = asyncio.Task(crawler(urls_q, proxies_q, proxies_q_good))
    task_proxies = asyncio.Task(find_proxies_async(urls_q, proxies_q, treads))
    loop.run_until_complete(asyncio.gather(task_crawler, task_proxies))
