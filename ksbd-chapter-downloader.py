#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def get_current_page_number(driver: webdriver.Firefox) -> str:
    return driver.find_element(By.CLASS_NAME, "paginav-current").text


#########################################################################################
def main():
    ### Static Vars
    BOOK_5_URL = "https://killsixbilliondemons.com/chapter/book-5-breaker-of-infinities/"
    # INDEX_URL = "https://killsixbilliondemons.com/wp-content/uploads/"

    ### Init
    print("==> Initialising driver")
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = webdriver.Firefox(
        options=driver_options,
    )

    print(f"==> Loading '{BOOK_5_URL}'")
    driver.get(BOOK_5_URL)


    #########################################################################################
    ### Get URLs for posts
    print("==> Fetching URLs for posts within given chapter")
    driver.find_element(By.LINK_TEXT, "Last »").click() ### For chronological order

    last_page = get_current_page_number(driver)

    post_urls = []
    while True:

        current_page = get_current_page_number(driver)
        print(f"==> Navigated to page {current_page} of {last_page}")

        ### Find
        posts = driver.find_elements(By.XPATH, "//*[@class='post-title']/a") ### Get "a"
        posts.reverse() ### For chronological order

        for post in posts:
            # print(post.text)
            print(post.get_attribute("href"))

            post_urls.append(post.get_attribute("href"))
        
        try:
            driver.find_element(By.LINK_TEXT, "«").click()
        except NoSuchElementException:
            break

    print(f"==> Found {len(post_urls)} post URLs")


    #########################################################################################
    ### Get URLs for posts

    # for url in post_urls()




if (__name__ == "__main__"):
    main()
