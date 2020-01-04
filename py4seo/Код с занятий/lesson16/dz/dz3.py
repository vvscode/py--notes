import aiohttp
import asyncio

from time import time
from concurrent.futures import ThreadPoolExecutor

from lxml import html
from aiopg.sa import create_engine

from db3 import Links, db_config


loop = asyncio.get_event_loop()
executor = ThreadPoolExecutor(max_workers=10)


async def moz_parser(urls_q):

    async with aiohttp.ClientSession() as session:

        while urls_q.qsize() > 0:
            url = await urls_q.get()
            try:
                async with session.get(url) as response:
                    html_code = await response.text()
            except Exception as e:
                print(type(e), e)
                await urls_q.put(url)
                continue

            dom_tree = await loop.run_in_executor(
                executor, html.fromstring, html_code)

            links = dom_tree.xpath('//h2/a')

            async with create_engine(**db_config) as engine:
                async with engine.acquire() as conn:
                    for link in links:

                        href = link.attrib['href']
                        name = link.text
                        await conn.execute(Links.insert().values(name=name, url=href))

                with open('results.txt', 'a', encoding='utf-8') as f:
                    f.write(f'{href}\t{name}\n')

            print(f'SUCCESS | {url}')


async def main():
    max_threads = 200

    base_url = 'https://moz.com/blog?page='
    all_pages = 385

    urls_queue = asyncio.Queue()

    for i in range(2, all_pages + 1):
        url = base_url + str(i)
        await urls_queue.put(url)

    tasks = []

    for _ in range(max_threads):
        task = moz_parser(urls_queue)
        tasks.append(task)

    t1 = time()
    await asyncio.gather(*tasks)
    t2 = time()

    print(t2 - t1)


if __name__ == '__main__':
    # uvloop.install()
    loop.run_until_complete(main())