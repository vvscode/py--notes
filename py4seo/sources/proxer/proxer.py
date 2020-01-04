import pdb
import re
import asyncio
import uvloop
import jinja2
import aiohttp
import aiohttp_jinja2
from aiohttp import web
from aiosocks.connector import ProxyConnector, ProxyClientRequest


# def proxy_generator():
#     for x1 in range(0, 255):
#         for x2 in range(0, 255):
#             for x3 in range(0, 255):
#                 for x4 in range(0, 255):
#                     for p in popular_ports:
#                         yield f'socks5://{x1}.{x2}.{x3}.{x4}:{p}'


async def worker(ipq):
    async with aiohttp.ClientSession(connector=ProxyConnector(), request_class=ProxyClientRequest) as http_client:
        while ipq.qsize():
            ip = await ipq.get()
            proxy = f'socks5://{ip}'
            # print('Scan:', proxy)
            try:
                resp = await http_client.get(_judge, proxy=proxy, timeout=4)
                assert resp.status == 200
                # print(ip)
                with open('proxies_working.txt', 'a', encoding='utf-8') as f:
                    f.write(ip+'\n')
            except Exception as e:
                # print(type(e), e)
                pass


async def crawler():
    while True:
        with open('proxies_working.txt', 'w', encoding='utf-8') as f:
            f.write('')

        ipq1 = asyncio.Queue()
        with open('proxies_fresh.txt', 'r', encoding='utf-8') as f:
            for p in f:
                ipq1.put_nowait(p.strip())
        parser_jobs = [asyncio.ensure_future(worker(ipq1)) for _ in range(_treads)]
        await asyncio.gather(*parser_jobs)

        ipq2 = asyncio.Queue()
        with open('proxies_all.txt', 'r', encoding='utf-8') as f:
            for p in f:
                ipq2.put_nowait(p.strip())
        parser_jobs = [asyncio.ensure_future(worker(ipq2)) for _ in range(_treads)]
        await asyncio.gather(*parser_jobs)


async def find_proxies():
    while True:
        if _flag:
            break

        with open('urls.txt', 'r', encoding='utf-8') as f:
            urls = [x.strip() for x in f if len(x.strip()) > 1]

        proxies_fresh = set()
        async with aiohttp.ClientSession() as http_client:
            for url in urls:
                try:
                    resp = await http_client.get(url, headers=_headers, timeout=60)
                    assert resp.status == 200, f'Can not get proxy source {url}'
                    code = await resp.text()
                    pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[ \t:]+(\d{2,5})'
                    pr = set(re.findall(pattern, code))
                    proxies_fresh = proxies_fresh.union(pr)
                except Exception as e:
                    # print(type(e), e)
                    pass

        with open('proxies_fresh.txt', 'w', encoding='utf-8') as f:
            for p in proxies_fresh:
                f.write(f'{p[0]}:{p[1]}\n')

        await asyncio.sleep(1)
        with open('proxies_all.txt', 'r', encoding='utf-8') as f:
            proxies_all = set([(x.strip().split(':')[0], x.strip().split(':')[1]) for x in f if x])

        await asyncio.sleep(1)
        with open('proxies_all.txt', 'w', encoding='utf-8') as f:
            proxies_all = proxies_all.union(proxies_fresh)
            for p in proxies_all:
                f.write(f'{p[0]}:{p[1]}\n')

        await asyncio.sleep(120)


def is_authenticated(handler):
    async def wrapper(request):
        key = request.GET.get('key')
        with open('keys.txt', 'r', encoding='utf-8') as f:
            keys = [x.strip().split()[0] for x in f]
        if key not in keys:
            return web.Response(text='Authenticatication Key Error', status=401)
        else:
            return await handler(request)
    return wrapper


async def main(request):
    response = aiohttp_jinja2.render_template('index.html', request, {})
    return response


@is_authenticated
async def fresh(request):
    with open('proxies_fresh.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    response = web.Response(text=data)
    response.headers["Content-Type"] = "text/plain"
    return response


@is_authenticated
async def working(request):
    with open('proxies_working.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    response = web.Response(text=data)
    response.headers["Content-Type"] = "text/plain"
    return response


@is_authenticated
async def get_all(request):
    with open('proxies_all.txt', 'r', encoding='utf-8') as f:
        data = f.read()
    response = web.Response(text=data)
    response.headers["Content-Type"] = "text/plain"
    return response


async def judge(request):
    text = ''
    for key, value in request._message.headers.items():
        text += key + ': ' + value + '\n'
    return web.Response(text=text)


async def _startup(app):
    asyncio.run_coroutine_threadsafe(find_proxies(), loop)
    asyncio.run_coroutine_threadsafe(crawler(), loop)


async def _shutdown(app):
    global _flag
    _flag = True


_flag = False
_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
_headers = {"User-Agent": _agent}
_judge = 'http://proxyjudge.us/azenv.php'
_treads = 200

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
loop = asyncio.get_event_loop()

app = web.Application(loop=loop)

app.on_startup.append(_startup)
app.on_shutdown.append(_shutdown)

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.router.add_static('/static', 'static', name='static')

app.router.add_route('GET', '/', main)
app.router.add_route('GET', '/fresh', fresh)
app.router.add_route('GET', '/working', working)
app.router.add_route('GET', '/judge', judge)
app.router.add_route('GET', '/all', get_all)

web.run_app(app, host='127.0.0.1', port=8008)
