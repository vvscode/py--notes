from pprint import pprint
from requests_html import HTMLSession


keyword = 'купить вентилятор'

session = HTMLSession()

resp = session.get(f'https://www.google.com/search?q={keyword}&num=100&hl=en')

# links = resp.html.xpath('//h3/a/@href')

links = resp.html.xpath('//div[@class="r"]/a[1]/@href')

domains = [x.split('/')[2] for x in links if 'http' in x]

# similar_keys = resp.html.xpath('//*[@id="brs"]/g-section-with-header/div[2]/div/p/node()/text()')
similar_keys = [element.text for element in resp.html.find('#extrares .card-section p')]

print('*'*50)
pprint(links)
print('*'*50)
pprint(domains)
print('*'*50)
pprint(similar_keys)
print('*'*50)

print(similar_keys)