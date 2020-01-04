import jinja2
import aiohttp_jinja2
from aiohttp import web, ClientSession
from lxml import html

from aiopg.sa import create_engine
from aiohttp_jinja2 import render_template

from db import dsn, Text


async def create_text(keyword, request):
    url = f'https://www.google.com/search?q={keyword}'
    headers = {'User-Agent': request.headers['User-Agent']}
    async with ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            html_code = await response.text()
    dom_tree = html.fromstring(html_code)
    snipets = dom_tree.xpath('//span[@class="st"]')
    text = ''
    for snip in snipets:
        text += ' ' + snip.text_content()
    return text


async def home_handler(request):
    pages = []
    async with request.app['db'].acquire() as conn:
        async for page in conn.execute(Text.select().limit(10)):
            pages.append(page)
    context = {
        'h1': 'Python Blog',
        'pages': pages
    }
    response = render_template('blog.html', request, context)
    return response


async def blog_page_handler(request):
    slug = request.match_info.get('slug', 'Python Blog')
    pages = []
    async with request.app['db'].acquire() as conn:
        async for page in conn.execute(
                Text.select().where(Text.c.slug == slug)):
            pages.append(page)

        if not pages:
            keyword = slug.replace('-', ' ')
            text = await create_text(keyword, request)
            data = {
                'key': keyword,
                'slug': slug,
                'text': text
            }
            await conn.execute(Text.insert().values(**data))

        else:
            page = pages[0]

            if not page.text:
                text = await create_text(page.key, request)
                data = {'text': text}
                await conn.execute(
                    Text.update().values(**data).where(Text.c.slug == slug))

        pages = []
        async for page in conn.execute(
                Text.select().where(Text.c.slug == slug)):
            pages.append(page)

    context = {
        'h1': pages[0].key.title(),
        'page': pages[0]
    }
    response = render_template('page.html', request, context)
    return response


async def robots_handler(request):
    with open('robots.txt') as f:
        text = f.read()
    return web.Response(text=text)


async def connect_to_db(app):
    app['db'] = await create_engine(dsn)


app = web.Application()

app.on_startup.append(connect_to_db)


aiohttp_jinja2.setup(
    app, loader=jinja2.FileSystemLoader('templates'))


app.add_routes(
    [
        web.get('/', home_handler),
        web.get('/robots.txt', robots_handler),
        web.get('/{slug}', blog_page_handler),
    ]
)

app.router.add_static(
    '/static/', path='static', name='static')


if __name__ == '__main__':
    web.run_app(app, host='127.0.0.1', port=5001)
