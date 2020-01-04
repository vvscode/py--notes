import pdb
import asyncio
import aiohttp
from aiopg.sa import create_engine as create_engine_async
from lxml import html
import sqlalchemy as sa
from datetime import date
from string import punctuation
from urllib.parse import quote
from aiosocks.connector import ProxyConnector, ProxyClientRequest
from pirat import headers, find_proxies_async


connection = {'user': '', 'database': '', 'host': '', 'password': ''}
dsn = 'postgresql://{user}:{password}@{host}/{database}'.format(**connection)

metadata = sa.MetaData()

Page = sa.Table(
    'bing', metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('keyword', sa.String(255)),
    sa.Column('wcount', sa.Integer),
    sa.Column('frequency', sa.Integer),
    sa.Column('url', sa.String(1023)),
    sa.Column('position', sa.Integer),
    sa.Column('title', sa.String(255)),
    sa.Column('h1', sa.String(255)),
    sa.Column('h2', sa.String(255)),
    sa.Column('text', sa.Text),
    sa.Column('html', sa.Text),
    sa.Column('date', sa.Date, default=date.today),
    sa.Column('company', sa.String(255)),
)


# base_link = 'https://www.google.com/search?q={}&num=100'
google_link = 'https://www.google.com/search?site=&source=hp&btnG=Search&q={}&num=100'
bing_link = 'https://www.bing.com/search?q={}&count=50'
# https://www.google.com.ua/search?q=info:https://www.elastic.co/guide/en/kibana/5.0/deb.html

treads = 100

gregulars = {'sites': '//h3/a/@href'}
bregulars = {'sites': '//h2/a/@href'}


def get_sites(code, keyword):
    tree = html.fromstring(code)
    result, sites = {}, []
    for element in bregulars:
        result[element] = tree.xpath(bregulars[element])
    if len(result['sites']) == 0:
        raise ValueError('No sites by keyword {}'.format(keyword[0]))
    for n, url in enumerate(result['sites'], start=1):
        sites.append({'keyword': keyword[0], 'wcount': keyword[1], 'frequency': keyword[2], 'url': url, 'position': n})
    return sites


async def worker(urls_q, proxies_q, proxies_q_good, db_client, http_client):
    while urls_q.qsize():
        if proxies_q_good.qsize():
            proxy = await proxies_q_good.get()
        else:
            if proxies_q.qsize():
                proxy = await proxies_q.get()
            else:
                await asyncio.sleep(1)
                continue
        # Get data from Queue
        key = await urls_q.get()
        key_str = key[0]
        for p in punctuation:
            key_str = key_str.replace(p, ' ').replace('  ', ' ').strip()
        url = bing_link.format(key_str.replace(' ', '+'))
        try:
            print(proxy.row, '-->', key[0], '| WPQ:', proxies_q_good.qsize(), '| APQ:', proxies_q.qsize())
        except:
            print(proxy.row, '-->', 'key', '| WPQ:', proxies_q_good.qsize(), '| APQ:', proxies_q.qsize())
        # Make http request with SOCKS proxy
        try:
            resp = await http_client.get(url, headers=headers, proxy=proxy.socks5, timeout=30)
            assert resp.status == 200
            code = await resp.text()
            assert len(code) > 10000
        except Exception as e:
            # print(type(e), e, '[worker, http_client.Exception]')
            await urls_q.put(key)
            continue
        # If proxy is working put it into good (working) proxies Queue again
        proxies_q_good.put_nowait(proxy)
        # Create dictionary data, to save it into database
        try:
            sites = get_sites(code, key)
            async with db_client.acquire() as conn:
                for site in sites:
                    await conn.execute(Page.insert().values(**site))
                    # print(site)
            print('[OK]', key[0])
        except Exception as e:
            print(type(e), e, '[data_formatting Exception]')
            continue


async def crawler(urls_q, proxies_q, proxies_q_good):
    async with create_engine_async(maxsize=treads, timeout=6000, **connection) as db_client:
        async with aiohttp.ClientSession(connector=ProxyConnector(), request_class=ProxyClientRequest) as http_client:
            parser_jobs = [asyncio.ensure_future(
                worker(urls_q, proxies_q, proxies_q_good, db_client, http_client))for _ in range(treads)]
            await asyncio.gather(*parser_jobs)


async def add_urls_to_queue(urls_q):
    t1 = time.time()
    normal_keys = set()
    all_keys = set()
    async with create_engine_async(timeout=6000, **connection) as db_client:
        async with db_client.acquire() as conn:
            async for key in conn.execute('select keyword from bing where position = 30;'):
                normal_keys.add(key[0])
            async for key in conn.execute('select keyword from bing where position = 1;'):
                all_keys.add(key[0])
            keys_to_delete = all_keys - normal_keys
            if len(keys_to_delete):
                await conn.execute("delete from bing where keyword in {};".format(tuple(keys_to_delete)))
    print('current_keys', len(normal_keys))
    print('keys_deleted', len(keys_to_delete))
    keys_in_file = dict()
    with open('data/big_keys.csv', 'r', encoding='utf-8') as infile:
        for line in infile:
            data = line.split(';')
            key = data[0]
            wcount = data[2] if data[2] else len(key.split())
            frequency = data[3] if data[3] else 0
            keys_in_file[key] = (wcount, frequency)
    my_keys = set(keys_in_file) - normal_keys
    for k in my_keys:
        urls_q.put_nowait((k, keys_in_file[k][0], keys_in_file[k][1]))
    print('Queue size:', urls_q.qsize())
    print('Queue itin time:', (time.time() - t1) / 60)


def creare_tables():
    engine = sa.create_engine(dsn)
    metadata.create_all(engine, tables=[Page])


def main():
    loop = asyncio.get_event_loop()
    urls_q = asyncio.Queue()
    proxies_q = asyncio.Queue()
    proxies_q_good = asyncio.Queue()
    loop.run_until_complete(add_urls_to_queue(urls_q))
    task_crawler = asyncio.Task(crawler(urls_q, proxies_q, proxies_q_good))
    task_proxies = asyncio.Task(find_proxies_async(urls_q, proxies_q, treads))
    loop.run_until_complete(asyncio.gather(task_crawler, task_proxies))


if __name__ == '__main__':
    # creare_tables()
    import time
    import gc
    while True:
        try:
            main()
        except Exception as e:
            print(type(e), e)
        time.sleep(10)
        gc.collect()
