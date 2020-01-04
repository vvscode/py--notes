from pprint import pprint
from requests_html import HTMLSession


keyword = 'online casino'

session = HTMLSession()
resp = session.get(f'https://www.google.com/search?q={keyword}&num=100&hl=en')

links = resp.html.xpath('//h3/a/@href')
domains = [x.split('/')[2] for x in links if 'http' in x]
similar_keys = resp.html.xpath('//div[@class="rc"]/div[2]/div/div[1]/div/text()')

print('*'*50)
pprint(links)
print('*'*50)
pprint(domains)
print('*'*50)
pprint(similar_keys)
print('*'*50)
