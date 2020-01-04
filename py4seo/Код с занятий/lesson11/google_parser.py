import random
from time import time, sleep
from requests_html import HTMLSession


PROXIES = []
GOOD_PROXIES = set()
TIMEOUT = 15
T1 = time()


def google_parser(keyword, proxy, user_agent):
    url = f'https://www.google.com.ua/search?q={keyword}&num=100'
    my_proxy = {'http': proxy, 'https': proxy}
    headers = {'User-Agent': user_agent}
    with HTMLSession() as session:
        resp = session.get(url, proxies=my_proxy, headers=headers, timeout=8)
        assert resp.status_code == 200
    return resp.html.xpath('//div[@class="r"]/a[1]/@href')


def get_random_agent():
    with open('UA.txt') as f:
        agents = [x.strip() for x in f]
    return random.choice(agents)


def get_proxy():
    global T1, PROXIES
    t2 = time()
    if ((t2-T1) > TIMEOUT) or not len(PROXIES):
        url = 'http://api.best-proxies.ru/proxylist.txt'
        params = {
            'key': 'b6e6bc8371eeabe14ab75b29464ab787',
            'type': 'socks4,socks5',
            # 'country': 'gb,us',
            'includeType': 1,
            'google': 1,
            'limit': 0
        }
        with HTMLSession() as session:
            response = session.get(url, params=params)
        PROXIES = response.text.split('\r\n')
        T1 = time()

    if len(GOOD_PROXIES) > 0:
        return random.choice(list(GOOD_PROXIES))
    else:
        return random.choice(PROXIES)


def main():
    with open('keys.txt') as f:
        keys = [line.strip() for line in f if line.strip()]

    for key in keys:

        while True:
            proxy = get_proxy()
            ua = get_random_agent()
            try:
                print(f'Send request to GOOGLE [{key}] from '
                      f'proxy: {proxy} and user_agent: {ua[:20]}')
                links = google_parser(key, proxy, ua)
                assert len(links) > 0
                break
            except Exception as e:
                print(type(e))

                if proxy in GOOD_PROXIES:
                    GOOD_PROXIES.remove(proxy)

        if links:
            if proxy not in GOOD_PROXIES:
                GOOD_PROXIES.add(proxy)

            with open('result.csv', 'a') as f2:
                for position, link in enumerate(links, start=1):
                    row = f'{key}\t{link}\t{position}\n'
                    f2.write(row)

        print(f'>>>>>>>> SUCCESS [{key}]')


if __name__ == '__main__':
    main()
