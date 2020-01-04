import pdb
import asyncio
import aiohttp
from lxml import html
from urllib.parse import quote
from aiosocks.connector import ProxyConnector, ProxyClientRequest
from pirat import headers, find_proxies_async


base_link = 'https://www.google.com.ua/search?q={}'
treads = 100


def get_keys(code):
    tree = html.fromstring(code)
    keys = set()
    for elem in tree.xpath('//p[@class="_e4b"]'):
        key = elem.text_content()
        keys.add(key)
    return keys


async def worker(urls_q, proxies_q, proxies_q_good, allkeys):
    while urls_q.qsize():
        if not proxies_q_good.empty():
            proxy = await proxies_q_good.get()
        else:
            if not proxies_q.empty():
                proxy = await proxies_q.get()
            else:
                await asyncio.sleep(1)
                continue
        key = await urls_q.get()
        url = base_link.format(quote(key))
        try:
            async with aiohttp.ClientSession(connector=ProxyConnector(), request_class=ProxyClientRequest) as http_client:
                async with http_client.get(url, headers=headers, proxy=proxy.socks5, timeout=30) as resp:
                    assert resp.status == 200
                    code = await resp.text()
            assert 'body' in code
        except Exception:
            # print(type(e), e, '[worker, http_client.Exception]')
            urls_q.put_nowait(key)
            continue
        proxies_q_good.put_nowait(proxy)
        try:
            keys = get_keys(code)
            for k in keys:
                if k not in allkeys:
                    allkeys.append(k)
                    # urls_q.put(k)
                    with open('data/google_suggests.txt', 'a', encoding='utf-8') as f:
                        f.write(k + '\n')
            print('[OK] {key}'.format(key=key))
        except Exception as e:
            # print(type(e), e, '[data_formatting Exception]')
            continue


async def crawler(urls_q, proxies_q, proxies_q_good):
    allkeys = list()
    with open('data/google_suggests.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if not line.strip():
                continue
            key = line.strip()
            allkeys.append(key)
            await urls_q.put(key)
    parser_jobs = [asyncio.ensure_future(worker(urls_q, proxies_q, proxies_q_good, allkeys))for _ in range(treads)]
    await asyncio.gather(*parser_jobs)


def main():
    loop = asyncio.get_event_loop()
    urls_q = asyncio.Queue()
    proxies_q = asyncio.Queue()
    proxies_q_good = asyncio.Queue()
    task_crawler = asyncio.Task(crawler(urls_q, proxies_q, proxies_q_good))
    task_proxies = asyncio.Task(find_proxies_async(urls_q, proxies_q, treads))
    loop.run_until_complete(asyncio.gather(task_crawler, task_proxies))


if __name__ == '__main__':
    main()
