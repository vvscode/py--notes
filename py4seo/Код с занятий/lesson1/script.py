from pprint import pprint
from requests_html import HTMLSession

session = HTMLSession()

resp = session.get('https://seoprofy.ua/blog')

links = resp.html.absolute_links
text = resp.html.text

print(links)
print('*'*50)
print(text)
print('*'*50)
pprint(dict(resp.headers))
print('*'*50)
