#!/usr/bin/python3

import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def get_current_page_no_number(driver: webdriver.Firefox) -> str:
    return driver.find_element(By.CLASS_NAME, "paginav-current").text

def get_post_urls(driver: webdriver.Firefox) -> list:
    """
    Navigates through pages of results for a given chapter.
    Returns a list of URLs for detected "posts"
    """

    print("==> Fetching URLs for posts within given chapter")
    driver.find_element(By.LINK_TEXT, "Last »").click() ### For chronological order

    last_page_no = get_current_page_no_number(driver)

    post_urls = []
    while True:

        current_page_no = get_current_page_no_number(driver)
        print(f"==> Navigated to page {current_page_no} of {last_page_no}")

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
            return post_urls
        
def navigate_pages(driver: webdriver.Firefox):
    """
    Navigates through pages of results for a given chapter.
    Loads page for any detected "posts".
    Downloads images
    """

    print("==> Fetching URLs for posts within given chapter")

    ### Calculate page URLs (without loading a new page)
    last_page_url = driver.find_element(By.LINK_TEXT, "Last »").get_attribute("href")
    last_page_no = int( re.search("[0-9]*\/$", last_page_url).group().replace("/", "") )

    page_urls = [f"{BOOK_5_URL}page/{i}" for i in range(last_page_no + 1)]
    page_urls[0] = BOOK_5_URL ### Correct first page
    page_urls.reverse()


    ### TODO: You know what to do haha
    for page_url in page_urls:
        driver.get(page_url)
        print(f"==> Navigated to page '{page_url}'")

        ### Detect "post" URLs
        posts = driver.find_elements(By.XPATH, "//*[@class='post-title']/a") ### Get "a"
        posts.reverse() ### For chronological order
        post_urls = [p.get_attribute("href") for p in posts]


        ### Iterate through posts
        for post_url in post_urls:
            driver.get(post_url)
            # print(f"==> Navigated to post '{post_url}'")

            imgs = driver.find_elements(
                By.XPATH,
                "//img[starts-with(@src,'https://killsixbilliondemons.com/wp-content/uploads/')]",
            )

            for img in imgs:
                print(img.get_attribute("src"))


#########################################################################################
### Globals
BOOK_5_URL = "https://killsixbilliondemons.com/chapter/book-5-breaker-of-infinities/"
# INDEX_URL = "https://killsixbilliondemons.com/wp-content/uploads/"


#########################################################################################
def main():

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
    ### TODO: MULTITHREAD

    # post_urls = get_post_urls(driver)
    # print(f"==> Found {len(post_urls)} post URLs")

    navigate_pages(driver)


    #########################################################################################
    ### Get URLs for posts
    ### TODO: MULTITHREAD

    # for post_url in post_urls():
    #     driver.get(post_url)

    #     comic_div = driver.find_element(By.XPATH, "//div[@id='comic']*")
    #     children_elements = comic_div.find_elements(By.XPATH, "*img")

    #     for possible_image in children_elements:
    #         if possible_image




if (__name__ == "__main__"):
    main()
