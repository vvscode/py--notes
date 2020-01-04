from pprint import pprint
from requests_html import HTMLSession


url = 'https://py4you.com/courses/python-for-seo/'

with HTMLSession() as session:
	resp = session.get(url)

title = resp.html.xpath('//title')[0].text
description = resp.html.xpath('//meta[@name="description"]/@content')


print('*'*20, 'title', '*'*20)
pprint(title)
print('*'*20, 'description', '*'*20)
pprint(description)
print('*'*50)