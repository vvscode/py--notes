import os
import random
from time import sleep
from lxml import html
from reppy.robots import Robots
from datetime import datetime
from selenium import webdriver

from db import Author, Ad, Category, db


with open('proxies.txt', 'r') as f:
    PROXIES = [x.strip() for x in f]


def get_browser(proxy=None):
    this_folder = os.getcwd()
    driver_ex = os.path.join(this_folder, 'chromedriver')
    options = webdriver.ChromeOptions()
    # options.add_argument(f'--proxy-server={proxy}')
    # options.add_argument('--headless')
    browser = webdriver.Chrome(executable_path=driver_ex, options=options)
    browser.set_window_position(0, 0)
    browser.set_window_size(1024, 768)
    browser.set_page_load_timeout(15)
    return browser


class Parser:

    def __init__(self, domain, schema):
        self.domain = domain
        self.schema = schema
        self.home_url = f'{self.schema}://{self.domain}'
        self.robots_url = self.home_url + '/robots.txt'
        self.real_domain = self.domain.split('/')[0]
        self.robots = Robots.fetch(self.robots_url)
        self.queue_urls = {self.home_url: 1}
        self.PARSED_URLS = set()
        self.browser = get_browser()

    def olx_ad_parser(self, url):
        is_ad = True if '/obyavlenie/' in url else False

        self.browser.get(url)
        sleep(5)

        if is_ad:
            phone_button = self.browser.find_element_by_xpath(
                '//div[contains(@class, "contact-button")]')
            phone_button.click()
            sleep(2)

        html_code = self.browser.page_source

        # browser.quit()

        dom_tree = html.fromstring(html_code)
        dom_tree.make_links_absolute(base_url=url)

        if is_ad:
            try:
                ad_name = dom_tree.xpath('//h1')[0].text.strip()
            except Exception as e:
                ad_name = 'not found'

            try:
                ad_price = dom_tree.xpath('//div[@class="price-label"]')[0].text_content().strip()
            except Exception as e:
                ad_price = 'not found'

            try:
                ad_image = dom_tree.xpath('//div[@id="photo-gallery-opener"]/img/@src')[0]
            except Exception as e:
                ad_image = 'not found'

            author = dom_tree.xpath('//div[@class="offer-user__details "]/h4/a')
            phone = dom_tree.xpath('//div[contains(@class, "contact-button")]/strong')[0].text

            author = {
                'name': author[0].text.strip(),
                'profile_link': author[0].attrib['href'],
                'phone': phone
            }

            db_author, created = Author.get_or_create(**author)

            categories = dom_tree.xpath('//td[@class="middle"]/ul/li/a')

            db_cats = []

            for n, cat in enumerate(categories):

                if n == 0:
                    parent = 0
                else:
                    parent = db_cats[n-1].id

                cat = {
                    'name': cat.text_content().strip(),
                    'link': cat.attrib['href'],
                    'parent': parent
                }

                cat, created = Category.get_or_create(**cat)
                db_cats.append(cat)

            print(db_cats)

            ad = {
                'author': db_author,
                'url': url,
                'name': ad_name.strip(),
                'price': ad_price,
                'image': ad_image,
                'date': datetime.now()
            }

            db_ad = Ad.create(**ad)

            for cat in db_cats:
                db_ad.categories.add(cat)

            print(ad)

        links = dom_tree.xpath('//a/@href')
        links = {x for x in links}

        return links

    def link_filter(self, link):
        if '#' in link:
            link = link.split('#')[0]
        if link.endswith('.jpg'):
            return False
        if self.real_domain not in link:
            return False
        if link in self.PARSED_URLS:
            return False
        if not self.robots.allowed(link, '*'):
            return False
        return True

    def parsing(self):
        with db.atomic():
            while len(self.PARSED_URLS) < 30:
                min_level = min(self.queue_urls.values())
                for url, level in self.queue_urls.items():
                    if level == min_level:
                        self.queue_urls.pop(url)
                        break
                print('Scan:', url, level)

                self.PARSED_URLS.add(url)

                links = self.olx_ad_parser(url)

                for link in links:
                    if not self.link_filter(link):
                        continue

                    if (link not in self.queue_urls) and ('/obyavlenie/' in link):
                        self.queue_urls[link] = level + 1


if __name__ == '__main__':

    domain = 'www.olx.ua'
    proto = 'https'

    url = 'https://www.olx.ua/obyavlenie/yarkaya-koftochka-IDGwsQM.html#95947f1cd8'

    pr = Parser(domain, proto)
    pr.olx_ad_parser(url)
