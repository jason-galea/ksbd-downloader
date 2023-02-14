#!/usr/bin/python3

import os
import re
from urllib import request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


#########################################################################################
### Functions
def calculate_page_urls():
    print("==> Started calculating page URLs")

    last_page_url = driver.find_element(By.LINK_TEXT, "Last »").get_attribute("href")
    last_page_no = int( re.search("[0-9]*\/$", last_page_url).group().replace("/", "") )

    page_urls = [f"{BOOK_5_URL}/page/{i}" for i in range(last_page_no + 1)]
    page_urls[0] = BOOK_5_URL ### Correct first page
    page_urls.reverse()

    print("==> Finished calculating page URLs")
    return page_urls

def scrape_post_urls(page_urls):
    print("==> Started scraping post URLs")

    post_urls = []
    for page_url in page_urls:
        driver.get(page_url)
        print(f"==> Navigated to page '{page_url}'")

        ### Detect "post" URLs
        posts = driver.find_elements(By.XPATH, "//*[@class='post-title']/a") ### Get "a"
        posts.reverse() ### For chronological order

        post_urls = post_urls + [p.get_attribute("href") for p in posts]

    print("==> Finished scraping post URLs")
    return post_urls

def scrape_image_urls(post_urls):
    print("==> Started scraping image URLs")

    image_urls = []
    for post_url in post_urls:
        driver.get(post_url)
        # print(f"==> Navigated to post '{post_url}'")

        imgs = driver.find_elements(
            by=By.XPATH,
            value=f"//img[starts-with(@src,'{WP_CONTENT_URL}')]",
        )
        image_urls = image_urls + [i.get_attribute("src") for i in imgs]

    print("==> Finished scraping image URLs")
    return image_urls
  
def download_images(image_urls):
    print("==> Started downloading images")

    download_prefix = 1
    for image_url in image_urls:
        filename = f"{DESTINATION_DIR}/{download_prefix}-{os.path.basename(image_url)}"

        print(f"==> Downloading '{image_url}' to '{filename}'")
        # request.urlretrieve(img_url, filename)

        download_prefix += 1
        
    print("==> Finished downloading images")


#########################################################################################
### Globals
BOOK_5_URL = "https://killsixbilliondemons.com/chapter/book-5-breaker-of-infinities"
WP_CONTENT_URL = "https://killsixbilliondemons.com/wp-content/uploads/"
DESTINATION_DIR = f"./downloads/{os.path.basename(BOOK_5_URL)}"


#########################################################################################
def main():


    ### Check/Create dir
    if not (os.path.exists(DESTINATION_DIR)):
        print(f"==> Creating destination directory '{DESTINATION_DIR}'")
        os.mkdir(DESTINATION_DIR)

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
    ### Begin
    page_urls = calculate_page_urls()
    print(page_urls)


    #########################################################################################
    ### Scrape post URLs
    post_urls = scrape_post_urls(page_urls)
    print(post_urls)


    #########################################################################################
    ### Scrape image URLs
    image_urls = scrape_image_urls(post_urls)
    print(image_urls)


    #########################################################################################
    ### Download images
    # download_images(image_urls)


if (__name__ == "__main__"):
    main()
