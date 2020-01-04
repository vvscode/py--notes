import os
from time import sleep
from selenium import webdriver


url = 'https://www.olx.ua/obyavlenie/reklama-v-metro-kiev-raskleyka-po-doskam-IDAB96v.html'


this_folder = os.getcwd()
driver_ex = os.path.join(this_folder, 'chromedriver')


options = webdriver.ChromeOptions()
options.add_argument('--headless')

browser = webdriver.Chrome(executable_path=driver_ex, options=options)

browser.get(url)

# sleep(2)

# phone_button = browser.find_element_by_xpath('//div[contains(@class, "contact-button")]')
# phone_button.click()
