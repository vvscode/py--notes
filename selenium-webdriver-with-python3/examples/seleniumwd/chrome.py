from selenium import webdriver
import os
import time


class RunChromeTests():
    # http://chromedriver.storage.googleapis.com/index.html

    def test(self):
        # driverLocation = "/Users/vvscode/Documents/repo/selenium/chromedriver"
        # os.environ["webdriver.chrome.driver"] = driverLocation

        # Instantiate Chrome Browser Command
        # driver = webdriver.Chrome(driverLocation)
        driver = webdriver.Chrome()
        # Open the provided URL
        driver.get("http://github.com/vvscode")
        time.sleep(10)


cht = RunChromeTests()
cht.test()
