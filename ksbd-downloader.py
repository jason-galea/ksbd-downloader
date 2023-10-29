#!/usr/bin/python3

import os
import json
# import pickle
# import argparse
import click

from urllib import request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


BOOKS_INFO: list = [
    {
        "name":                 "kill-six-billion-demons",
        "title":                "Kill Six Billion Demons",
        "chapters": [
            {
                "start_url":    "https://killsixbilliondemons.com/comic/kill-six-billion-demons-chapter-1/",
                "end_url":      "https://killsixbilliondemons.com/comic/ksbd-1-17/"
            },
            {
                "start_url":    "https://killsixbilliondemons.com/comic/ksbd-2-0/",
                "end_url":      "https://killsixbilliondemons.com/comic/prim-leaves-her-fathers-house/"
            },
            {
                "start_url":    "https://killsixbilliondemons.com/comic/chapter-3/",
                "end_url":      "https://killsixbilliondemons.com/comic/ksbd-3-53-54/"
            },
            {
                "start_url":    "https://killsixbilliondemons.com/comic/kill-six-billion-demons-chapter-4/",
                "end_url":      "https://killsixbilliondemons.com/comic/aesma-and-the-three-masters-part-3-and-4/"
            },
            {
                "start_url":    "https://killsixbilliondemons.com/comic/ksbd-5-1/",
                "end_url":      "https://killsixbilliondemons.com/comic/ksbd-5-89-to-5-90/"
            },
        ]
    },
    {
        "name":                 "wielder-of-names",
        "title":                "Wielder of Names",
        "chapters": [
            {
                "start_url":    "https://killsixbilliondemons.com/comic/wielder-of-names-cover/",
                "end_url":      "https://killsixbilliondemons.com/comic/wielder-of-names-1-18/"
            },
            {
                "start_url":    "https://killsixbilliondemons.com/comic/wielder-of-names-2-19/",
                "end_url":      "https://killsixbilliondemons.com/comic/wielder-of-names-2-39-pursuers/"
            },
            {
                "start_url":    "https://killsixbilliondemons.com/comic/wielder-of-names-3-39/",
                "end_url":      "https://killsixbilliondemons.com/comic/wielder-of-names-3-59/"
            },
            {
                "start_url":    "https://killsixbilliondemons.com/comic/wielder-of-names-4-60-palace-of-radiance/",
                "end_url":      "https://killsixbilliondemons.com/comic/wielder-of-names-4-80/"
            },
            {
                "start_url":    "https://killsixbilliondemons.com/comic/wielder-of-names-5-81/",
                "end_url":      "https://killsixbilliondemons.com/comic/wielder-of-names-5-102/"
            },
            {
                "start_url":    "https://killsixbilliondemons.com/comic/wielder-of-names-6-103-to-6-104-war-of-the-teacups/",
                "end_url":      "https://killsixbilliondemons.com/comic/wielder-of-names-6-123/"
            },
        ]
    },
    {
        "name":                 "seek-of-thrones",
        "title":                "Seeker of Thrones",
        "chapters": [
            {
                "start_url":    "",
                "end_url":      ""
            },
        ]
    },
    {
        "name":                 "king-of-swords",
        "title":                "King of Swords",
        "chapters": [
            {
                "start_url":    "",
                "end_url":      ""
            },
        ]
    },
    {
        "name":                 "breaker-of-infinities",
        "title":                "Breaker of Infinities",
        "chapters": [
            {
                "start_url":    "",
                "end_url":      ""
            },
        ]
    },
    {
        "name":                 "wheel-smashing-lord",
        "title":                "Wheel Smashing Lord",
        "chapters": [
            {
                "start_url":    "",
                "end_url":      ""
            },
        ]
    }
]


@click.command()
# @click.argument("book", type=click.IntRange(min=1, max=6, min_open=False, max_open=False, clamp=False) )
@click.option("-b", "--book", type=int, help="Book # to download, from 1-6.")
@click.option("-c", "--chapter", type=int, help="Chapter # to download. Defaults to downloading all chapters")
@click.option("--only_get_details", is_flag=True, help="")
@click.option("--only_get_images", is_flag=True, help="")
def main(book: int, chapter: int, only_get_details: bool, only_get_images: bool):

    CWD = os.getcwd()
    DOWNLOAD_DIR = f"{CWD}/out"


    ### Args
    print(f"==> DEBUG: book = {book}")
    print(f"==> DEBUG: chapter = {chapter}")
    print(f"==> DEBUG: get_details = {only_get_details}")
    print(f"==> DEBUG: get_images = {only_get_images}")

    if not book:
        exit(f"==> ERROR: Please provide the number of the book to download, from 1-6")
    
    if not chapter:
        print(f"==> INFO: No chapter specified, defaulting to all chapters")
        chapters = list(range(len(BOOKS_INFO))) ### 0-5
    else:
        chapters = [chapter-1] ### BOOKS_INFO is zero-indexed

    if (only_get_details and only_get_images):
        exit(f"==> ERROR: You must download either page details or images, exiting early")


    ### Check/Create dir
    if not (os.path.exists(DOWNLOAD_DIR)):
        print(f"==> INFO: Creating download directory '{DOWNLOAD_DIR}'")
        os.makedirs(DOWNLOAD_DIR)

    
    for c in chapters:
        
        ### Get details
        if not only_get_details:
            pass
            # temp_champter_details = [
            #     ### Page 1
            #     {
            #         "title":        "",
            #         "entry_html":   "",
            #         "alt_text":     "",
            #         "image_urls":   [
            #             "...",
            #             "...",
            #         ],
            #     },
            #     ### Page ...
            #     {},
            # ]
            temp_champter_details = get_chapter_details(**BOOKS_INFO[book]["chapters"][c])
        

    
        ### Get images
        if not only_get_images:
            pass




    # ### Detect existing image_urls.txt file
    # if (os.path.exists(IMAGE_URLS_FILE)):
    #     print(f"==> INFO: Reading URLs from existing file")
    #     with open(IMAGE_URLS_FILE, "rb") as f:
    #         image_urls = f.read().strip("\n").split("\n")

    # else:
    #     print(f"==> INFO: Did not detect existing image URLs file")
    #     print(f"==> INFO: Scraping image URLs")
    #     image_urls = scrape_image_urls()

    # # print(f"DEBUG: image_urls = {image_urls}")
    # print(f"==> INFO: Found {len(image_urls)} URLs")

    # download_images(image_urls)

    # print(f"==> INFO: ALL DONE!!!!")


def get_chapter_details(start_url: str, end_url: str):
    print(f"==> DEBUG: start_url = {start_url}")
    print(f"==> DEBUG: end_url = {end_url}")



# def scrape_image_urls():

#     ### Create webdriver
#     print("==> INFO: Initialising webdriver")
#     driver_options = Options()
#     driver_options.add_argument("--headless")
#     driver = webdriver.Firefox(
#         options=driver_options,
#     )

#     ### Scrape image URLs
#     # print(f"==> INFO: Scraping image URLs")
#     driver.get(FIRST_PAGE)

#     image_urls = []
#     while True:
#         print(f"==> INFO: Navigated to '{driver.current_url}'")

#         ### Find image elements
#         img_elements = driver.find_elements(
#             by=By.XPATH,
#             value="//img[contains(@src,'killsixbilliondemons.com/wp-content/uploads/')]",
#         )

#         ### Save URLs to list (Without printing)
#         # image_urls += [i.get_attribute("src") for i in img_elements]

#         ### Save URLs to list (With printing)
#         temp_image_urls = [i.get_attribute("src") for i in img_elements]
#         for image_url in temp_image_urls:
#             print(f"==> INFO: Found image URL '{image_url}'")
#         image_urls += temp_image_urls

#         ### Boilerplate
#         if (driver.current_url != LAST_PAGE):
#             driver.find_element(By.LINK_TEXT, "Next >").click()
#         else:
#             print(f"==> INFO: Finished scraping URLs")
#             break

#     ### Save image URLs to disk
#     print(f"==> INFO: Saving image URLs to disk")
#     with open(IMAGE_URLS_FILE, "wb") as f:
#         # pickle.dump(image_urls, f)
#         f.write('\n'.join(image_urls))

#     return image_urls


# def download_images(image_urls):

#     ### Detect page no. zfill length
#     page_no_zfill_length = len(str( len(image_urls) - 1 )) ### -1 so cover page no. = 0
#     print(f"==> Detected page no. zfill length of {page_no_zfill_length}")

#     ### Download images
#     for page_no, image_url in enumerate(image_urls):
        
#         # filename = f"{DOWNLOAD_DIR}/{os.path.basename(image_url)}"
#         page_no_zfilled = str(page_no).zfill(page_no_zfill_length)
#         image_basename = os.path.basename(image_url)
#         filename = f"{DOWNLOAD_DIR}/{page_no_zfilled}-{image_basename}"

#         ### Don't redownload images from previous runs
#         if not (os.path.exists(filename)):
#             print(f"==> Downloading '{image_url}' to '{os.path.basename(filename)}'")
#             request.urlretrieve(image_url, filename)
#         else:
#             print(f"==> WARNING: File '{os.path.basename(filename)}' already exists")

#         # print(f"==> Downloading '{image_url}' to '{os.path.basename(filename)}'")
#         # request.urlretrieve(image_url, filename)


if (__name__ == "__main__"):
    main()
