import os
from lxml import html
from selenium import webdriver
import pdb

start_link = 'https://www.amazon.com/gp/search/other/ref=sr_sa_p_n_theme_browse-bin?rh=n%3A2858778011&bbn=2858778011&pickerToList=theme_browse-bin&ie=UTF8&qid=1496146252'


def get_cats():
    chrome_driver = os.path.join(os.getcwd(), 'chromedriver.exe')
    browser = webdriver.Chrome(executable_path=chrome_driver)
    browser.get(start_link)
    tree = html.fromstring(browser.page_source)
    browser.quit()
    cat_hrefs = tree.xpath('//a[@class="a-link-normal"]/@href')
    cats = list()
    for cat in cat_hrefs:
        cat = 'https://www.amazon.com' + cat
        cats.append(cat)
        for i in range(2, 401):
            cats.append(cat + '&page={}'.format(i))
    return cats


def get_films():
    cats = get_cats()
    chrome_driver = os.path.join(os.getcwd(), 'chromedriver.exe')
    browser = webdriver.Chrome(executable_path=chrome_driver)
    for cat in cats:
        browser.get(cat)
        tree = html.fromstring(browser.page_source)
        film_hrefs = tree.xpath('//div[contains(@class,"a-row")]/a[contains(@class, "s-access-detail-page")]/@href')
        with open('film_links.txt', 'a', encoding='utf-8') as f:
            for film in film_hrefs:
                film = str(film)[:str(film).index('ref=')]
                f.write(film+'\n')
    browser.quit()


if __name__ == '__main__':
    get_films()
