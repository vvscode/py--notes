from pprint import pprint
from requests_html import HTMLSession


keyword = 'online casino'

session = HTMLSession()

resp = session.get(f'https://www.google.com/search?q={keyword}&num=100&hl=en')

# links = resp.html.xpath('//h3/a/@href')

links = resp.html.xpath('//div[@class="r"]/a[1]/@href')

domains = [x.split('/')[2] for x in links if 'http' in x]

similar_keys = resp.html.xpath('//div[@class="exp-c"]/a/text()')

print('*'*50)
pprint(links)
print('*'*50)
pprint(domains)
print('*'*50)
pprint(similar_keys)
print('*'*50)

print(similar_keys)
