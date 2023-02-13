#!/usr/bin/python3

# import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

def download_by_chapter(driver, url):
    driver.get(url)
    driver.find_element(By.LINK_TEXT, "Last »").click()

    ### Loop through all pages of results (backwards, to sort chronologically)
    while True:
        
        ### Get list of posts
        posts = driver.find_elements(By.CLASS_NAME, "post-title")
        posts.reverse() ### Again, reverse to get chronological order

        for post in posts:
            print(post.text)


        # ### Get image URLs
        # images = driver.find_elements(By.CLASS_NAME, "attachment-large size-large wp-post-image")

        # for image in images:
        #     print(image.get_attribute("src"))


        ### Next page of posts
        # os.wait(1)
        driver.find_element(By.LINK_TEXT, "«").click()

def download_by_index(driver, url):
    driver.get(url)

    # driver.find_element(By.LINK_TEXT, "Last »").click()

def main():
    
    BOOK_5_URL = "https://killsixbilliondemons.com/chapter/book-5-breaker-of-infinities/"
    INDEX_URL = "https://killsixbilliondemons.com/wp-content/uploads/"

    ### Init
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = webdriver.Firefox(
        options=driver_options,
    )

    ### Start navigating & downloading
    # download_by_chapter(driver, BOOK_5_URL)
    download_by_chapter(driver, INDEX_URL)

if (__name__ == "__main__"):
    main()
