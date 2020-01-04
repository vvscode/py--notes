import requests
from lxml import html
from parser3 import olx_ad_parser


url = 'https://www.olx.ua/moda-i-stil/kiev/'


custom_headers = {
    'Accept-Language': 'en-US,en;q=0.9,uk;q=0.8,ru;q=0.7,fr;q=0.6',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Ubuntu Chromium/78.0.3904.108 '
                  'Chrome/78.0.3904.108 Safari/537.36'
}


response = requests.get(url, headers=custom_headers)

html_dom = html.fromstring(response.text)


product_urls = html_dom.xpath('//h3/a/@href')


for url in product_urls:

    try:
        ad = olx_ad_parser(url)
    except requests.exceptions.Timeout:
        ad = {}

    print(ad)
