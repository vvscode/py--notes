from time import time
from requests_html import HTMLSession


PARSED_URLS = set()


def url_parser(url):
    with HTMLSession() as session:
        t1 = time()
        response = session.get(url, proxies={})
        t2 = time()
    try:
        title = response.html.xpath('//title')[0].text
    except Exception as e:
        title = 'not_found'
    try:
        h1 = response.html.xpath('//h1')[0].text
    except Exception as e:
        h1 = 'not_found'
    resp_time = round(t2 - t1, 2)
    links = response.html.absolute_links

    return title, h1, resp_time, links


def link_filter(link, domain, robots):
    if '#' in link:
        link = link.split('#')[0]
    if link.endswith('.jpg'):
        return False
    if domain not in link:
        return False
    if link in PARSED_URLS:
        return False
    if not robots.allowed(link, '*'):
        return False
    return True


if __name__ == '__main__':
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    print(__name__)
    print('AAAAAAAAAAAAAAAAAAAAAAAAAAAA')
