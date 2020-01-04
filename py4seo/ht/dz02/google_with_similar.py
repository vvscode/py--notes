# function
from pprint import pprint

# type
from requests_html import HTMLSession

# str
keyword = input("Введите ключевое слово: ")

# requests_html.HTMLSessio
session = HTMLSession()

# requests_html.HTMLResponse
resp = session.get(f"https://www.google.com/search?q={keyword}&num=100&hl=en")

# list
links = resp.html.xpath('//div[@class="r"]/a[1]/@href')

# list
domains = [x.split("/")[2] for x in links if "http" in x]

# list
similar_elements = resp.html.xpath('//div[@class="card-section"]//p')

# list
similar_keys = [el.text.strip() for el in similar_elements]

print("*" * 50)
pprint(links)
print("*" * 50)
pprint(domains)
print("*" * 50)
pprint(similar_keys)
print("*" * 50)
