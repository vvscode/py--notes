import os
import re
from time import sleep
from urllib.parse import unquote
from selenium import webdriver
from lxml import html
from datetime import datetime

from db import GoogleImage, db


def get_google_images(key):
    url = f'https://www.google.com/search?q={key}&tbm=isch'

    this_folder = os.getcwd()
    driver_ex = os.path.join(this_folder, 'chromedriver')

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')

    browser = webdriver.Chrome(executable_path=driver_ex, options=options)
    browser.get(url)
    sleep(2)
    dom_tree = html.fromstring(browser.page_source)
    browser.quit()

    hrefs = dom_tree.xpath('//a[@class="rg_l"]/@href')
    links = []

    for href in hrefs:
        try:
            found = re.search('imgurl=(.+?)&imgrefurl', href).group(1)
            image_url = unquote(found)
            links.append(image_url)
        except Exception as e:
            print(e, type(e))

    return links


def main():
    keywords = ['php', 'shmeo', 'files']

    for k in keywords:
        image_urls = get_google_images(k)
        parse_time = datetime.now()

        imgs = []

        for image in image_urls:
            img_data = {'keyword': k, 'image_url': image,
                        'date': parse_time}

            imgs.append(GoogleImage(**img_data))

            # GoogleImage.create(**img_data)

            # GoogleImage.create(
            #     keyword=k,
            #     image_url=image,
            #     date=parse_time
            # )

        with db.atomic():
            GoogleImage.bulk_create(imgs)

        print('parsed', k, len(imgs))


def read_from_db():
    data_from_database = GoogleImage.select().where(GoogleImage.id < 10)

    for image in data_from_database:

        image.keyword = 'AAAAAAAAAAAAAA_' + image.keyword
        image.save()

        print(image.keyword, image.image_url)


def update_in_db():
    result = GoogleImage.update(keyword='python').where(GoogleImage.id < 10).execute()
    print(result)


def delete_from_db():
    GoogleImage.delete().where(GoogleImage.id < 10).execute()


if __name__ == '__main__':
    # kw = input('Enter keyword: ')
    # image_urls = get_google_images(kw)
    # print(image_urls)
    # breakpoint()
    main()
    # read_from_db()
    # update_in_db()
    # delete_from_db()
