import asyncio
from time import sleep

from requests_html import AsyncHTMLSession


async def moz_parser(urls_q):
    session = AsyncHTMLSession()

    while urls_q.qsize() > 0:
        url = await urls_q.get()
        try:
            response = await session.get(url)

            sleep(5)

        except Exception as e:
            print(type(e), e)
            await urls_q.put(url)
            continue

        links = response.html.xpath('//h2/a')

        for link in links:

            href = link.attrs['href']
            name = link.text

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

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
