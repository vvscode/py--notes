from selenium import webdriver
from selenium.webdriver.common.by import By
import time

baseUrl = "https://letskodeit.teachable.com/pages/practice"
driver = webdriver.Firefox()
driver.get(baseUrl)


class FindByIdName():

    def test(self):
        elementById = driver.find_element_by_id("name")

        if elementById is not None:
            print("We found an element by Id")

        elementByName = driver.find_element_by_name("show-hide")

        if elementByName is not None:
            print("We found an element by Name")


class FindByXPathCSS():

    def test(self):
        elementByXpath = driver.find_element_by_xpath("//input[@id='name']")

        if elementByXpath is not None:
            print("We found an element by XPATH")

        elementByCss = driver.find_element_by_css_selector("#displayed-text")

        if elementByCss is not None:
            print("We found an element by CSS")


class FindByLinkText():

    def test(self):
        elementByLinkText = driver.find_element_by_link_text("Login")

        if elementByLinkText is not None:
            print("We found an element by Link Text")

        elementByPartialLinkText = driver.find_element_by_partial_link_text("Pract")

        if elementByPartialLinkText is not None:
            print("We found an element by Partial Link Text")


class FindByClassTag():

    def test(self):
        elementByClassName = driver.find_element_by_class_name("displayed-class")
        elementByClassName.send_keys('Hola')

        if elementByClassName is not None:
            print("We found an element by Class Name")

        elementByTagName = driver.find_element_by_tag_name("h1")

        if elementByTagName is not None:
            print("We found an element by Tag Name and the text on element is: " + elementByTagName.text)


class ByDemo():

    def test(self):
        elementById = driver.find_element(By.ID, "name")

        if elementById is not None:
            print("We found an element by Id")

        elementByXpath = driver.find_element(By.XPATH, "//input[@id='displayed-text']")

        if elementByXpath is not None:
            print("We found an element by XPATH")

        elementByLinkText = driver.find_element(By.LINK_TEXT, "Login")

        if elementByLinkText is not None:
            print("We found an element by Link Text")


class ListOfElements():

    def test(self):
        elementListByClassName = driver.find_elements_by_class_name("inputs")
        length1 = len(elementListByClassName)

        if elementListByClassName is not None:
            print("ClassName -> Size of the list is: " + str(length1))

        elementListByTagName = driver.find_elements(By.TAG_NAME, "td")
        length2 = len(elementListByTagName)

        if elementListByTagName is not None:
            print("TagName -> Size of the list is: " + str(length2))


for cls in [FindByIdName, FindByXPathCSS, FindByLinkText, FindByClassTag, ByDemo, ListOfElements]:
    example = cls()
    example.test()
