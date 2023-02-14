#!/usr/bin/python3

import os
import re
from urllib import request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def main():

    ### Vars
    BOOK_5_URL = "https://killsixbilliondemons.com/chapter/book-5-breaker-of-infinities"
    DESTINATION_DIR = f"./downloads/{os.path.basename(BOOK_5_URL)}"
    download_prefix = 1

    ### Check/Create dir
    if not (os.path.exists(DESTINATION_DIR)):
        print(f"==> Creating destination directory '{DESTINATION_DIR}'")
        os.mkdir(DESTINATION_DIR)

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

    print("==> Fetching URLs for posts within given chapter")

    ### Calculate page URLs (without loading a new page)
    last_page_url = driver.find_element(By.LINK_TEXT, "Last »").get_attribute("href")
    last_page_no = int( re.search("[0-9]*\/$", last_page_url).group().replace("/", "") )

    page_urls = [f"{BOOK_5_URL}/page/{i}" for i in range(last_page_no + 1)]
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
                by=By.XPATH,
                value="//img[starts-with(@src,'https://killsixbilliondemons.com/wp-content/uploads/')]",
            )
            img_urls = [i.get_attribute("src") for i in imgs]

            for img_url in img_urls:
                filename = f"{DESTINATION_DIR}/{download_prefix}-{os.path.basename(img_url)}"

                print(f"==> Downloading '{img_url}' to '{filename}'")
                # request.urlretrieve(img_url, filename)

                download_prefix += 1


if (__name__ == "__main__"):
    main()
