from selenium import webdriver
from selenium.webdriver.common.by import By
import time 

link = "http://suninjuly.github.io/find_xpath_form"

try:
    browser = webdriver.Chrome()
    browser.get(link)

    first_name = browser.find_element(By.NAME, 'first_name')
    first_name.send_keys("Ivan")

    last_name = browser.find_element(By.NAME, 'last_name')
    last_name.send_keys("Ivan")

    city = browser.find_element(By.CLASS_NAME, 'city')
    city.send_keys("Ivan")

    country = browser.find_element(By.ID, 'country')
    country.send_keys("Ivan")

    submit_button = browser.find_element(By.XPATH, '//button[text()="Submit"]')
    submit_button.click()

finally:
    # успеваем скопировать код за 30 секунд
    time.sleep(30)
    # закрываем браузер после всех манипуляций
    browser.quit()