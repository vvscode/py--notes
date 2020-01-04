import os
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

LOGIN = 'ТВОЙ МЭЙЛ'
PASSWORD = 'ТВОЙ ПАРОЛЬ'


chrome_path = os.path.join(os.getcwd(), 'chromedriver')


def find_in_bing(browser, keyword):
    keyword = keyword.replace(' ', '+')
    start = 1
    while start <= 1001:
        bing_link = f'https://www.bing.com/search?q=site%3Ahttps%3A%2F%2Fru.linkedin.com%2Fin%2F+{keyword}' \
                    f'&count=50&first={start}'
        browser.get(bing_link)
        friends = browser.find_elements_by_xpath('//h2/a')
        try:
            friends = [(frd.text.split('-')[0].strip(), frd.get_property('href')) for frd in friends]
        except Exception as e:
            print(e)
            continue
        print(len(friends))
        with open('friends.csv', 'a') as file:
            for name, link in friends:
                try:
                    print(name, link)
                    file.write(f'{name}\t{link}\n')
                    browser.get(link)
                    connect = browser.find_element_by_xpath(
                        '//span/button[contains(@class,"profile-actions") and contains(@class, "connect")]')
                    connect.click()
                    sleep(0.5)
                    invite_now = browser.find_element_by_xpath(
                        '//div[@class="send-invite__actions"]/button[contains(@class,"button-primary-large")]')
                    invite_now.click()
                    sleep(2)
                    print('Invite was sended')
                except Exception as e:
                    print(e)
        start += 50


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
    find_in_bing(browser, 'seo')


if __name__ == '__main__':
    go()
