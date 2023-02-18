#!/usr/bin/python3

import os
import re
from urllib import request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By



def main():

    ### Vars
    ### NOTE: These extras are for testing only, using them will break the filename prefix
    # FIRST_COMIC = "https://killsixbilliondemons.com/comic/king-of-swords-174-177-finale/"
    # FIRST_COMIC = "https://killsixbilliondemons.com/comic/breaker-of-infinities-1-9-to-1-10/"
    # FIRST_COMIC = "https://killsixbilliondemons.com/comic/breaker-of-infinities-1-37-to-1-38/"
    # FIRST_COMIC = "https://killsixbilliondemons.com/comic/breaker-of-infinities-3-82-to-3-83/"

    FIRST_COMIC = "https://killsixbilliondemons.com/comic/kill-six-billion-demons-breaker-of-infinities/"
    LAST_COMIC = "https://killsixbilliondemons.com/comic/breaker-of-infinities-4-182-to-4-183/"
    DOWNLOAD_DIR = "./downloads/book-5-breaker-of-infinities"
    # PAGE_NO = 0 ### "0" for the cover page
    # PAGE_NO_LENGTH = 4 ### "1-page" --> "0001-page"
    

    ### Help text
    # print(f"==> This script will download all pages from:")
    # print(f"==> \t'{FIRST_COMIC}'")
    # print(f"==> To:")
    # print(f"==> \t'{LAST_COMIC}'")
    # print(f"==> They will be downloaded to directory: '{DOWNLOAD_DIR}'")
    # print()

    ### Check/Create dir
    if not (os.path.exists(DOWNLOAD_DIR)):
        print(f"==> Creating destination directory '{DOWNLOAD_DIR}'")
        os.mkdir(DOWNLOAD_DIR)

    ### Create webdriver
    print("==> Initialising webdriver")
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = webdriver.Firefox(
        options=driver_options,
    )

    ### Initial load
    print(f"==> Loading FIRST_COMIC: '{FIRST_COMIC}'")
    driver.get(FIRST_COMIC)

    ### Scrape image URLs
    print(f"==> Scraping image URLs")
    image_urls = []
    while True:
        print(f"==> Navigated to '{driver.current_url}'")

        ### Find image elements
        img_elements = driver.find_elements(
            by=By.XPATH,
            value="//img[contains(@src,'killsixbilliondemons.com/wp-content/uploads/')]",
        )

        ### Save URLs to list
        image_urls += [i.get_attribute("src") for i in img_elements]

        ### Boilerplate
        if (driver.current_url != LAST_COMIC):
            driver.find_element(By.LINK_TEXT, "Next >").click()
        else:
            # print(f"==> Reached LAST_COMIC: {LAST_COMIC}")
            print(f"==> Finished scraping image URLs")
            break

    ### Detect page no. zfill length
    page_no_zfill_length = len(image_urls) - 1 ### -1 to make the cover page no. = 0

    ### Download images
    for page_no, image_url in enumerate(image_urls):
        
        # filename = f"{DOWNLOAD_DIR}/{os.path.basename(image_url)}"
        page_no_zfilled = str(page_no).zfill(page_no_zfill_length)
        image_basename = os.path.basename(image_url)
        filename = f"{DOWNLOAD_DIR}/{page_no_zfilled}-{image_basename}"

        # if not (os.path.exists(filename)):
        #     print(f"==> Downloading '{image_url}' to '{filename}'")
        #     request.urlretrieve(image_url, filename)
        # else: ### NOTE: Does this actually happen?
        #     print(f"==> WARNING: File '{filename}' already exists")

        print(f"==> Downloading '{image_url}' to '{filename}'")
        # request.urlretrieve(image_url, filename)


if (__name__ == "__main__"):
    main()
