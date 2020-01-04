from pprint import pprint
from requests_html import HTMLSession


keyword = input('Введите ключевое слово: ')
domain = input('Введите домен: ')

session = HTMLSession()

resp = session.get(
	f'https://www.google.com/search?q={keyword}&num=100&hl=en')

links = resp.html.xpath('//div[@class="r"]/a[1]/@href')

for position, url in enumerate(links, start=1):
	if domain in url:
		print(f'Position for website {domain} is {position}')
