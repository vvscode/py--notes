from selenium import webdriver
from selenium.webdriver.common.by import By
import time 
import math

crypted_link_text = str(math.ceil(math.pow(math.pi, math.e)*10000))
link = "http://suninjuly.github.io/find_link_text"

try:
    browser = webdriver.Chrome()
    browser.get(link)

    crypted_link = browser.find_element_by_partial_link_text(crypted_link_text)
    crypted_link.click()

    first_name = browser.find_element(By.NAME, 'first_name')
    first_name.send_keys("Ivan")

    last_name = browser.find_element(By.NAME, 'last_name')
    last_name.send_keys("Ivan")

    city = browser.find_element(By.CLASS_NAME, 'city')
    city.send_keys("Ivan")

    country = browser.find_element(By.ID, 'country')
    country.send_keys("Ivan")

    submit_button = browser.find_element(By.TAG_NAME, 'button')
    submit_button.click()

finally:
    # успеваем скопировать код за 30 секунд
    time.sleep(30)
    # закрываем браузер после всех манипуляций
    browser.quit()