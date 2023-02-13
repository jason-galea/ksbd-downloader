from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui

def main():
    driver = webdriver.Firefox()
    driver.get('https://www.google.com/')

    page_url=driver.find_elements_by_xpath("//a[@class='content']")
    all_title = driver.find_elements_by_class_name("title")
    title = [title.text for title in all_title]

    print(title)


if (__name__ == "__main__"):
    main()
