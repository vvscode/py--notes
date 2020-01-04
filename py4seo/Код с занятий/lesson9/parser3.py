import random
from requests_html import HTMLSession


proxies = [
    {'http': '123.123.123.132', 'https': '234.234.234.234'},
    {'http': '124.123.123.132', 'https': '234.234.234.234'},
    {'http': '125.123.123.132', 'https': '234.234.234.234'},
    {'http': '126.123.123.132', 'https': '234.234.234.234'},
    {'http': '127.123.123.132', 'https': '234.234.234.234'},
]


def olx_ad_parser(url):
    custom_headers = {
        'Accept-Language': 'en-US,en;q=0.9,uk;q=0.8,ru;q=0.7,fr;q=0.6',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Ubuntu Chromium/78.0.3904.108 '
                      'Chrome/78.0.3904.108 Safari/537.36'
    }

    my_random_proxy = random.choice(proxies)
    print(my_random_proxy)

    with HTMLSession() as session:
        response = session.get(
            url,
            headers=custom_headers,
            # proxies=my_random_proxy,
            timeout=0.2
        )

    name = response.html.xpath('//h1')[0].text

    try:
        price = response.html.xpath('//strong[@class="xxxx-large not-arranged"]')[0].text
    except Exception as e:
        print(e, type(e))
        price = 'not found'

    try:
        image = response.html.xpath('//div[@id="photo-gallery-opener"]/img/@src')[0]
    except Exception as e:
        print(e, type(e))
        image = 'not found'

    ad = {
        'name': name.strip(),
        'price': price,
        'image': image
    }
    return ad
