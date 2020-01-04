import pdb
import jinja2
import aiohttp_jinja2
from aiohttp import web, ClientSession
from lxml import html


async def content_generator(keyword):
    url = f'https://www.bing.com/search?q={keyword}'.replace(' ', '+')
    async with ClientSession() as session:
        async with await session.get(url) as resp:
            html_text = await resp.text()
    dom_tree = html.fromstring(html_text)
    snipets = dom_tree.xpath('//div[@class="b_caption"]/p/text()')
    generated_text = ' '.join(snipets)
    return generated_text


async def main(request):
    context = {'key': 'Main Page', 'text': 'some text'}
    response = aiohttp_jinja2.render_template('index.html', request, context)
    return response


async def page(request):
    key = request.match_info.get('key')
    key = key.replace('-', ' ').title()
    text = await content_generator(key)
    context = {'h1': key, 'text': text}
    response = aiohttp_jinja2.render_template('page.html', request, context)
    return response


app = web.Application()

app.add_routes([web.get('/', main)])
app.add_routes([web.get('/{key}', page)])


aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app.router.add_static('/static', 'static', name='static')

jenv = app.get('aiohttp_jinja2_environment')


web.run_app(app, host='127.0.0.1', port=8000)
