from selenium import webdriver


class RunFFTests():

    def test(self):
        # Instantiate FF Browser Command
        driver = webdriver.Firefox()
        # Open the provided URL
        driver.get("http://github.com/vvscode")


ff = RunFFTests()
ff.test()
