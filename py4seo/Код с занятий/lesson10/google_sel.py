import os
from pprint import pprint

from lxml import html

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


keyword = input('Введите ключевое слово: ')

this_folder = os.getcwd()
driver_ex = os.path.join(this_folder, 'chromedriver')

options = webdriver.ChromeOptions()
options.add_argument('--headless')

browser = webdriver.Chrome(executable_path=driver_ex, options=options)
url = f'https://www.google.com/'
browser.get(url)

q_input = browser.find_element_by_name('q')

q_input.send_keys(keyword)
q_input.send_keys(Keys.ENTER)

html_code = browser.page_source

dom_tree = html.fromstring(html_code)

links = dom_tree.xpath('//div[@class="r"]/a[1]/@href')
domains = [x.split('/')[2] for x in links if 'http' in x]

similar_elements = dom_tree.xpath('//div[@class="card-section"]//p')
similar_keys = [el.text_content().strip() for el in similar_elements]


browser.quit()

print('*'*50)
pprint(links)
print('*'*50)
pprint(domains)
print('*'*50)
pprint(similar_keys)
print('*'*50)
