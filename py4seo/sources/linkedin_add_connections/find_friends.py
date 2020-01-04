import os
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

LOGIN = 'ТВОЙ МЭЙЛ'
PASSWORD = 'ТВОЙ ПАРОЛЬ'


chrome_path = os.path.join(os.getcwd(), 'chromedriver')


def go():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(executable_path=chrome_path, options=chrome_options)

    browser.set_page_load_timeout(60)
    url = 'https://www.linkedin.com/'
    browser.get(url)
    sleep(random.randint(1, 3))
    login = browser.find_element_by_id("login-email")
    login.clear()
    login.send_keys(LOGIN)
    sleep(1)
    password = browser.find_element_by_id("login-password")
    password.clear()
    password.send_keys(PASSWORD)
    sleep(1)
    password.send_keys('\ue007')
    sleep(random.randint(1, 3))
    filter_link = "https://www.linkedin.com/search/results/people/v2/?" \
                  "facetGeoRegion=[%22by%3A0%22]&" \
                  "facetNetwork=[%22S%22]&" \
                  "facetProfileLanguage=[%22ru%22]&" \
                  "keywords=seo&" \
                  "origin=FACETED_SEARCH"

    start_page = 29
    browser.get(filter_link+f'&page={start_page}')
    sleep(1)

    results = browser.find_elements_by_xpath('//div/h3')

    count = None
    for h3 in results:
        print(h3.text)
        if 'result' in str(h3.text):
            count = str(h3.text).replace(',', '').split()[1]
            count = int(count)
            pages = count // 10 + 1
            print(count, pages)

    if not count:
        raise ValueError('Cant Find results count')

    for page in range(start_page, 100):
        browser.find_element_by_tag_name('html').send_keys(Keys.END)
        sleep(1)
        browser.find_element_by_tag_name('html').send_keys(Keys.HOME)
        sleep(1)
        connections = browser.find_elements_by_xpath('//div/button[contains(@class,"search-result")]')
        for conn in connections:
            if conn.text == 'Connect':
                try:
                    browser.execute_script("arguments[0].scrollIntoView();", conn)
                    sleep(0.5)
                    browser.execute_script(f"window.scrollBy(0, -200);")
                    sleep(0.5)
                    conn.click()
                    sleep(0.5)
                    invite_now = browser.find_element_by_xpath('//div[@class="send-invite__actions"]/button[contains(@class,"button-primary-large")]')
                    invite_now.click()
                    sleep(2)
                    print('Invite was sended on page', page)
                except Exception as e:
                    print(type(e), e, f'on page {page}')
        browser.get(filter_link+f'&page={page+1}')
        sleep(1)


if __name__ == '__main__':
    go()
