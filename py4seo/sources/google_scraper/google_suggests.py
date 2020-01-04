import os
from lxml import html
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from queue import Queue
import pdb

TREADS = 5
GOOGLE = 'https://www.google.com.ua/'
# PROXY = 'ip'
LOCK = Lock()


def get_data(code):
    tree = html.fromstring(code)
    keys = set()
    for elem in tree.xpath('//div[@class="sbqs_c"]'):
        key = elem.text_content()
        keys.add(key)
    return keys


def worker(q, allkeys):
    chrome_driver = os.path.join(os.getcwd(), 'chromedriver.exe')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
    chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument('--proxy-server={}'.format(PROXY))
    # isalert = expected_conditions.alert_is_present()
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver)
    browser.set_page_load_timeout(40)
    browser.get(GOOGLE)
    sleep(1)
    while q.qsize():
        key = q.get()
        se = browser.find_element_by_name("q")
        se.clear()
        se.send_keys(key)
        se.click()
        sleep(1)
        keys = get_data(browser.page_source)
        with LOCK:
            for k in keys:
                if k not in allkeys:
                    allkeys.append(k)
                    q.put(k)
                    with open('data\\google_suggests.txt', 'a') as f:
                        f.write(k + '\n')
    browser.quit()


def main():
    q = Queue()
    with open('data\\google_suggests.txt', 'r') as f:
        allkeys = f.read().split('\n')
    for k in allkeys:
        q.put(k)
    with ThreadPoolExecutor(max_workers=TREADS) as executor:
        for _ in range(TREADS):
            executor.submit(worker, q, allkeys)


if __name__ == '__main__':
    main()
