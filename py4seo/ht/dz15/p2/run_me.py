# На диске в папке https://drive.google.com/drive/u/0/folders/1UvubgSa5s827kQhIRKvg8o-SVBdvWTZ_
# Лежит файл as_parser2.py.
# Взять этот файл и реализовать сохранение спаршенных данных (href, name)
# в этом асинхронном парсере в базу данных.
# Используем Aiopg (+ SQLAlchemy) https://aiopg.readthedocs.io/en/stable/.
import aiohttp
import asyncio

from time import time

from concurrent.futures import ThreadPoolExecutor
from lxml import html

import db

loop = asyncio.get_event_loop()
executor = ThreadPoolExecutor(max_workers=10)


async def moz_parser(urls_q, save_data):

    async with aiohttp.ClientSession() as session:

        while urls_q.qsize() > 0:
            url = await urls_q.get()
            print(f"Start processing {url}")
            try:
                async with session.get(url) as response:
                    html_code = await response.text()

                # await asyncio.sleep(5)

            except Exception as e:
                print(type(e), e)
                await urls_q.put(url)
                continue

            dom_tree = await loop.run_in_executor(executor, html.fromstring, html_code)

            links = dom_tree.xpath("//h2/a")

            # with locker:
            await save_data(
                list(
                    map(
                        lambda link: {
                            "url": link.attrib["href"],
                            "name": link.text,
                            "page_url": url,
                        },
                        links,
                    )
                )
            )

            print(f"SUCCESS | {url}")


async def main():
    max_threads = 200
    # max_threads = 2
    base_url = "https://moz.com/blog?page="
    all_pages = 385
    # all_pages = 8
    save_data, close_connection = await db.get_data_saver()

    urls_queue = asyncio.Queue()

    for i in range(2, all_pages + 1):
        url = base_url + str(i)
        await urls_queue.put(url)

    tasks = []

    for _ in range(max_threads):
        task = moz_parser(urls_queue, save_data)
        tasks.append(task)

    t1 = time()
    await asyncio.gather(*tasks)
    t2 = time()
    await close_connection()

    print(t2 - t1)


if __name__ == "__main__":
    # uvloop.install()
    loop.run_until_complete(main())
