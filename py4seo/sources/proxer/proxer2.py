import pdb
import time
import asyncio
import uvloop
import aiohttp
from aiosocks.connector import ProxyConnector, ProxyClientRequest


popular_ports = [
    1080, 1032, 1924, 1978, 2081, 2827, 4160, 4207, 4471, 4537, 4954, 5015, 5057, 5337, 5443, 5498, 5630,
    5679, 5718, 5871, 6032, 6087,  6159, 6171, 6292, 6560, 6896, 7014,  7155, 7166, 7209, 7596, 7758, 7770,
    8486, 8544, 8984, 9366, 9560, 9617, 9726, 9998, 10798, 11218, 11480, 11839, 11903, 12165, 12429, 12721,
    12794, 12994, 13273, 15481, 15621, 15979, 16120, 16717, 17040, 17702, 17773, 18449, 18924, 19787, 20318,
    20399, 20582, 21514, 21679, 21705, 21984, 22346, 22623, 45554, 7824, 8065
]


url = 'http://proxyjudge.us/azenv.php'
# url = 'http://google.com/'

treads = 400

counter = 0


# def proxy_generator():
#     for x1 in range(0, 255):
#         for x2 in range(0, 255):
#             for x3 in range(0, 255):
#                 for x4 in range(0, 255):
#                     for p in popular_ports:
#                         yield f'socks5://{x1}.{x2}.{x3}.{x4}:{p}'


def proxy_generator():
    with open('proxies_all.txt', 'r', encoding='utf-8') as f:
        for line in f:
            yield f'socks5://{line.strip()}'


async def worker(ipq):
    global counter
    async with aiohttp.ClientSession(connector=ProxyConnector(), request_class=ProxyClientRequest) as http_client:
        while ipq.qsize():
            ip = ipq.get()
            proxy = f'socks5://{ip}'
            counter += 1
            # print('Scan:', proxy, counter)
            try:
                resp = await http_client.get(url, proxy=proxy, timeout=4)
                assert resp.status == 200
                print(proxy, counter)
            except Exception as e:
                # print(type(e), e)
                pass


async def crawler():
    gen = proxy_generator()
    parser_jobs = [asyncio.ensure_future(worker(gen)) for _ in range(treads)]
    await asyncio.gather(*parser_jobs)


def main():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(crawler())


if __name__ == '__main__':
    main()
