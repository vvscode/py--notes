from urllib.request import urlopen
import requests
from lxml import html

from requests_html import HTMLSession


url = 'https://www.moyo.ua/telecommunication/mini_ats/ats-bazovie-bloki/'


custom_headers = {
    'Accept-Language': 'en-US,en;q=0.9,uk;q=0.8,ru;q=0.7,fr;q=0.6',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Ubuntu Chromium/78.0.3904.108 '
                  'Chrome/78.0.3904.108 Safari/537.36'
}


response = requests.get(url, headers=custom_headers)

html_dom = html.fromstring(response.text)


products = html_dom.xpath(
    '//div[@class="catalog-content"]//div[contains(@class, "product-tile_title")]/a')

prices = html_dom.xpath(
    '//div[@class="catalog-content"]//'
    'div[@class="product-tile_price-current"]/span[2]/span[1]')


result = dict()

for i, product in enumerate(products):
    key = product.text.strip()
    try:
        value = prices[i].text.strip().replace('\xa0', '')
        value = int(value)
    except IndexError:
        value = 0
    result[key] = value


sort_iphones = sorted(result.items(), key=lambda x: x[1])


with HTMLSession() as session:
    response2 = session.get(url)
