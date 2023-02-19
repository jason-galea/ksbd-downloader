#!/usr/bin/python3

import os
import re
from urllib import request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


def main():

    ### Vars
    ### NOTE: Obviously these test vars will give incorrect page number prefixes
    # FIRST_COMIC = "https://killsixbilliondemons.com/comic/king-of-swords-174-177-finale/"
    # FIRST_COMIC = "https://killsixbilliondemons.com/comic/breaker-of-infinities-1-9-to-1-10/"
    # FIRST_COMIC = "https://killsixbilliondemons.com/comic/breaker-of-infinities-1-37-to-1-38/"
    # FIRST_COMIC = "https://killsixbilliondemons.com/comic/breaker-of-infinities-3-82-to-3-83/"
    LAST_COMIC = "https://killsixbilliondemons.com/comic/breaker-of-infinities-1-9-to-1-10/"

    FIRST_COMIC = "https://killsixbilliondemons.com/comic/kill-six-billion-demons-breaker-of-infinities/"
    # LAST_COMIC = "https://killsixbilliondemons.com/comic/breaker-of-infinities-4-182-to-4-183/"

    CWD = os.getcwd()
    FIRST_COMIC_BASENAME = os.path.basename(FIRST_COMIC)
    LAST_COMIC_BASENAME = os.path.basename(LAST_COMIC)
    IMAGE_URLS_FILE = f"{CWD}/downloads/image_urls_{FIRST_COMIC_BASENAME}_to_{LAST_COMIC_BASENAME}.txt"
    DOWNLOAD_DIR = f"{CWD}/downloads/book-5-breaker-of-infinities"
    

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
        os.makedirs(DOWNLOAD_DIR)

    ### Create webdriver
    print("==> Initialising webdriver")
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = webdriver.Firefox(
        options=driver_options,
    )

    ### Detect existing image_urls.txt file
    if (os.path.exists(IMAGE_URLS_FILE)):
        print(f"==> Detected existing image URLs file '{IMAGE_URLS_FILE}'")

        ### Split filename to compare FIRST_COMIC and LAST_COMIC
        image_urls_filename_split = os.path.basename(IMAGE_URLS_FILE).removeprefix("image_urls_").split("_to_")
        
        if (image_urls_filename_split[0] != FIRST_COMIC_BASENAME):
            print(f"==> FIRST_COMIC from image URLs filename did not match, continuing to scrape image URLs")
            pass
        if (image_urls_filename_split[1] != LAST_COMIC_BASENAME):
            print(f"==> LAST_COMIC from image URLs filename did not match, continuing to scrape image URLs")
            pass

    else:
        print(f"==> Did not detect existing IMAGE_URLS_FILE, continuing to scrape image URLs")
        pass

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
        [print(i.get_attribute("src")) for i in img_elements]
        image_urls += [i.get_attribute("src") for i in img_elements]

        ### Boilerplate
        if (driver.current_url != LAST_COMIC):
            driver.find_element(By.LINK_TEXT, "Next >").click()
        else:
            # print(f"==> Reached LAST_COMIC: {LAST_COMIC}")
            print(f"==> Scraped {len(image_urls)} URLs")
            break

    # print(f"==> DEBUG: image_urls = {image_urls}")

    ### Save image URLs to disk
    print(f"==> Saving image URLs to disk")
    with open(IMAGE_URLS_FILE, "w") as f:
        f.writelines(image_urls)

    ### Detect page no. zfill length
    page_no_zfill_length = len(str( len(image_urls) - 1 )) ### -1 so cover page no. = 0
    print(f"==> Detected page no. zfill length of {page_no_zfill_length}")

    ### Download images
    for page_no, image_url in enumerate(image_urls):
        
        # filename = f"{DOWNLOAD_DIR}/{os.path.basename(image_url)}"
        page_no_zfilled = str(page_no).zfill(page_no_zfill_length)
        image_basename = os.path.basename(image_url)
        filename = f"{DOWNLOAD_DIR}/{page_no_zfilled}-{image_basename}"

        ### Don't redownload images from previous runs
        if not (os.path.exists(filename)):
            print(f"==> Downloading '{image_url}' to '{os.path.basename(filename)}'")
            request.urlretrieve(image_url, filename)
        else:
            print(f"==> WARNING: File '{filename}' already exists")

        # print(f"==> Downloading '{image_url}' to '{os.path.basename(filename)}'")
        # request.urlretrieve(image_url, filename)


if (__name__ == "__main__"):
    main()
