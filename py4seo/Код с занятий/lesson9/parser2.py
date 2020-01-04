import requests
from lxml import html


url = 'https://www.moyo.ua/telecommunication/mini_ats/ats-bazovie-bloki/'


custom_headers = {
    'Accept-Language': 'en-US,en;q=0.9,uk;q=0.8,ru;q=0.7,fr;q=0.6',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Ubuntu Chromium/78.0.3904.108 '
                  'Chrome/78.0.3904.108 Safari/537.36'
}


response = requests.get(url, headers=custom_headers)

html_dom = html.fromstring(response.text)


products_divs = html_dom.xpath(
    '//div[@class="catalog-content"]//section[contains(@class, "product-tile_product")]')


result = dict()


for block in products_divs:
    try:
        name = block.xpath('.//div[contains(@class, "product-tile_title")]/a')[0].text
        name = name.strip()
    except:
        name = 'Unknown Product'
    try:
        price = block.xpath('.//div[@class="product-tile_price-current"]/span[2]/span[1]')[0].text
        price = price.replace('\xa0', '')
        price = int(price)
    except:
        price = 'not found'

    result[name] = price


print(result)
