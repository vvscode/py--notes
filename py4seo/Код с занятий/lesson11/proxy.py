from requests_html import HTMLSession


url = 'http://api.best-proxies.ru/proxylist.txt'

params = {
    'key': 'b6e6bc8371eeabe14ab75b29464ab787',
    'type': 'socks4,socks5',
    'country': 'gb,us',
    'includeType': 1,
    'limit': 0
}


with HTMLSession() as session:
    response = session.get(url, params=params)
    proxies = response.text.split('\r\n')


breakpoint()
