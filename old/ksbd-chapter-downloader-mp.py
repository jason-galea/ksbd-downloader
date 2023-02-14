#!/usr/bin/python3

import re
from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


#########################################################################################
### Functions
def process_pages(page_url):
    driver.get(page_url)
    print(f"==> Navigated to page '{page_url}'")

    ### Detect "post" URLs
    posts = driver.find_elements(By.XPATH, "//*[@class='post-title']/a") ### Get "a"
    posts.reverse() ### For chronological order
    post_urls = [p.get_attribute("href") for p in posts]


    ### Iterate through posts
    # for post_url in post_urls:
    #     process_posts(post_url)
    with Pool(4) as p:
        p.map(process_posts, post_urls)

def process_posts(post_url):
    driver.get(post_url)
    # print(f"==> Navigated to post '{post_url}'")

    ### Search for images within post
    ### NOTE: 9/10 times this is a single image
    imgs = driver.find_elements(
        By.XPATH,
        "//img[starts-with(@src,'https://killsixbilliondemons.com/wp-content/uploads/')]",
    )

    for img in imgs:
        print(img.get_attribute("src"))


#########################################################################################
### Globals
BOOK_5_URL = "https://killsixbilliondemons.com/chapter/book-5-breaker-of-infinities/"


#########################################################################################
def main():

    ### Init
    print("==> Initialising driver")
    driver_options = Options()
    driver_options.add_argument("--headless")

    global driver
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

    page_urls = [f"{BOOK_5_URL}page/{i}" for i in range(last_page_no + 1)]
    page_urls[0] = BOOK_5_URL ### Correct first page
    page_urls.reverse()


    ### Iterate through pages
    for page_url in page_urls:
        process_pages(page_url)
    # with Pool(4) as p:
    #     p.map(process_pages, page_urls)


if (__name__ == "__main__"):
    main()
