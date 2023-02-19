#!/usr/bin/python3

import os
import pickle
from urllib import request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


################################################################################################
### FUNCTIONS
def scrape_image_urls():

    ### Create webdriver
    print("==> Initialising webdriver")
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = webdriver.Firefox(
        options=driver_options,
    )

    ### Scrape image URLs
    # print(f"==> Scraping image URLs")
    driver.get(FIRST_PAGE)

    image_urls = []
    while True:
        print(f"==> Navigated to '{driver.current_url}'")

        ### Find image elements
        img_elements = driver.find_elements(
            by=By.XPATH,
            value="//img[contains(@src,'killsixbilliondemons.com/wp-content/uploads/')]",
        )

        ### Save URLs to list (Without printing)
        # image_urls += [i.get_attribute("src") for i in img_elements]

        ### Save URLs to list (With printing)
        temp_image_urls = [i.get_attribute("src") for i in img_elements]
        for image_url in temp_image_urls:
            print(f"==> Found image URL '{image_url}'")
        image_urls += temp_image_urls

        ### Boilerplate
        if (driver.current_url != LAST_PAGE):
            driver.find_element(By.LINK_TEXT, "Next >").click()
        else:
            print(f"==> Finished scraping URLs")
            break

    ### Save image URLs to disk
    print(f"==> Saving image URLs to disk")
    with open(IMAGE_URLS_FILE, "wb") as f:
        pickle.dump(image_urls, f)

    return image_urls

def download_images(image_urls):

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
            print(f"==> WARNING: File '{os.path.basename(filename)}' already exists")

        # print(f"==> Downloading '{image_url}' to '{os.path.basename(filename)}'")
        # request.urlretrieve(image_url, filename)


################################################################################################
### GLOBALS
### NOTE: Obviously these test vars will give incorrect page number prefixes
# FIRST_PAGE = "https://killsixbilliondemons.com/comic/king-of-swords-174-177-finale/"
# FIRST_PAGE = "https://killsixbilliondemons.com/comic/breaker-of-infinities-1-9-to-1-10/"
# FIRST_PAGE = "https://killsixbilliondemons.com/comic/breaker-of-infinities-1-37-to-1-38/"
# FIRST_PAGE = "https://killsixbilliondemons.com/comic/breaker-of-infinities-3-82-to-3-83/"
# LAST_PAGE = "https://killsixbilliondemons.com/comic/breaker-of-infinities-1-9-to-1-10/"
# LAST_PAGE = "https://killsixbilliondemons.com/comic/breaker-of-infinities-1-37-to-1-38/"

# ### Book 5: Breaker of Infinities
# FIRST_PAGE = "https://killsixbilliondemons.com/comic/kill-six-billion-demons-breaker-of-infinities/"
# LAST_PAGE = "https://killsixbilliondemons.com/comic/breaker-of-infinities-4-182-to-4-183/"
# BOOK_TITLE = "book-5-breaker-of-infinities"

### Book 6: Wheel Smashing Lord
FIRST_PAGE = "https://killsixbilliondemons.com/comic/kill-six-billion-demons-wheel-smashing-lord/"
LAST_PAGE = "https://killsixbilliondemons.com/comic/wheel-smashing-lord-1-3/"
BOOK_TITLE = "book-6-wheel-smashing-lord"

CWD = os.getcwd()
FIRST_PAGE_BASENAME = os.path.basename( FIRST_PAGE.removesuffix("/") ).replace("_", "-")
LAST_PAGE_BASENAME = os.path.basename( LAST_PAGE.removesuffix("/") ).replace("_", "-")
IMAGE_URLS_FILE = f"{CWD}/downloads/image_urls_{FIRST_PAGE_BASENAME}_to_{LAST_PAGE_BASENAME}.txt"
DOWNLOAD_DIR = f"{CWD}/downloads/{BOOK_TITLE}"
HELP_TEXT = f"""
==> This script will download all pages from:
==> \t'{FIRST_PAGE}
==> To:
==> \t'{LAST_PAGE}
==> They will be downloaded to directory: '{DOWNLOAD_DIR}
"""

# print(f"DEBUG: LAST_PAGE = {LAST_PAGE}")
# print(f"DEBUG: LAST_PAGE_BASENAME = {LAST_PAGE_BASENAME}")
# print(f"DEBUG: FIRST_PAGE = {FIRST_PAGE}")
# print(f"DEBUG: FIRST_PAGE_BASENAME = {FIRST_PAGE_BASENAME}")
# print(f"DEBUG: IMAGE_URLS_FILE = {IMAGE_URLS_FILE}")
# print(f"DEBUG: DOWNLOAD_DIR = {DOWNLOAD_DIR}")


################################################################################################
def main():
    print(HELP_TEXT)

    ### Check/Create dir
    if not (os.path.exists(DOWNLOAD_DIR)):
        print(f"==> Creating download directory '{DOWNLOAD_DIR}'")
        os.makedirs(DOWNLOAD_DIR)

    ### Detect existing image_urls.txt file
    if (os.path.exists(IMAGE_URLS_FILE)):
        print(f"==> Reading URLs from existing file")
        with open(IMAGE_URLS_FILE, "rb") as f:
            image_urls = pickle.load(f)

    else:
        print(f"==> Did not detect existing image URLs file")
        print(f"==> Scraping image URLs")
        image_urls = scrape_image_urls()

    # print(f"DEBUG: image_urls = {image_urls}")
    print(f"==> Found {len(image_urls)} URLs")

    download_images(image_urls)

    print(f"==> ALL DONE!!!!")


if (__name__ == "__main__"):
    main()
