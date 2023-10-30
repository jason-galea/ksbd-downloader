#!/usr/bin/python3

import os
import json
import click
# import pickle
# import argparse

# from urllib import request
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
                # "end_url":      "https://killsixbilliondemons.com/comic/ksbd-chapter-1-1/"
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
@click.option("--dont_get_details", is_flag=True, help="Only download page details, ignoring images")
@click.option("--dont_get_images", is_flag=True, help="Only download images, assuming image URLs are known")
@click.option("--force_get_details", is_flag=True, help="Ignore previously downloaded details")
@click.option("--force_get_images", is_flag=True, help="Ignore previously downloaded images")
def main(
    book: int,
    chapter: int,
    dont_get_details: bool,
    dont_get_images: bool,
    force_get_details: bool,
    force_get_images: bool
):

    ### Args
    if not book:
        exit(f"==> ERROR: Please provide the number of the book to download, from 1-6")
    
    if not chapter:
        print(f"==> INFO: No chapter specified, defaulting to all chapters")
        chapters = list(range(len(BOOKS_INFO))) ### 0-5
    else:
        chapters = [chapter-1] ### BOOKS_INFO is 0-indexed

    if (dont_get_details and dont_get_images):
        exit(f"==> ERROR: You must download either page details or images, exiting early")


    ### Vars
    CWD = os.getcwd()
    DOWNLOAD_DIR = f"{CWD}/out"
    BOOK_DIR = f"{CWD}/out/{book}-{BOOKS_INFO[book-1]['name']}"

    # print(f"==> DEBUG: book = {book}")
    # print(f"==> DEBUG: chapter = {chapter}")
    # print(f"==> DEBUG: get_details = {dont_get_details}")
    # print(f"==> DEBUG: get_images = {dont_get_images}")
    # print(f"==> DEBUG: CWD = {CWD}")
    print(f"==> DEBUG: DOWNLOAD_DIR = {DOWNLOAD_DIR}")
    print(f"==> DEBUG: BOOK_DIR = {BOOK_DIR}")
    print()


    ### Create dirs
    # create_dirs(DOWNLOAD_DIR)
    # create_dirs(BOOK_DIR)

    
    ### Create webdriver
    print("==> INFO: Initialising webdriver")
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = webdriver.Firefox(
        options=driver_options,
    )

    
    for c in chapters:
        
        chapter_dir = f"{BOOK_DIR}/{c+1}"
        chapter_details_file = f"{BOOK_DIR}/{c+1}/details.json"

        create_dirs(chapter_dir)

        if force_get_details:
            try:
                os.remove(chapter_details_file)
            except FileNotFoundError:
                pass


        ### Get details
        if not os.path.exists(chapter_details_file):

            if not dont_get_details:
                chapter_details = get_chapter_details(driver, **BOOKS_INFO[book-1]["chapters"][c])

                print(f"==> INFO: Writing chapter details to '{chapter_details_file}'")
                with open(chapter_details_file, "w") as f:
                    f.write(json.dumps(chapter_details, indent=4))

            else:
                print(f"==> INFO: Skip getting chapter details due to 'dont_get_details'")

        else:
            print(f"==> INFO: Detected existing chapter details file '{chapter_details_file}'")
            with open(chapter_details_file, "r") as f:
                chapter_details = json.load(f)


        print(f"==> DEBUG: chapter_details = {json.dumps(chapter_details, indent=4)}")

        
        ### Get images
        if not dont_get_images:
            get_chapter_images(chapter_dir, chapter_details)


def create_dirs(dir_path: str):
    if not (os.path.exists(dir_path)):
        print(f"==> INFO: Creating directory '{dir_path}'")
        os.makedirs(dir_path)


def get_chapter_details(driver: webdriver.Firefox, start_url: str, end_url: str) -> list:
    print(f"==> DEBUG: Entered get_chapter_details()")

    driver.get(start_url)

    chapter_details = []
    while True:
        # print(f"==> DEBUG: Navigated to '{driver.current_url}'")

        title_ele = driver.find_element(By.CLASS_NAME, "post-title")

        entry_ele = driver.find_element(By.CLASS_NAME, "entry")
        entry_ele_children = entry_ele.find_elements(By.CSS_SELECTOR, "*")
        entry_ele_children_extracted = []

        for e in entry_ele_children:
            if e.tag_name == "p":
                entry_ele_children_extracted.append(e.text)
            elif (e.tag_name == "a") and ("title" in e.__dict__.keys()):
                entry_ele_children_extracted.append(e.title)
            elif e.tag_name == "img":
                entry_ele_children_extracted.append(e.get_attribute("src"))

        img_eles = driver.find_elements(By.XPATH,
            "//img[contains(@src,'killsixbilliondemons.com/wp-content/uploads/')]",
        )
        
        temp_page_details = {
            "title":        title_ele.text,
            "image_urls":   [i.get_attribute("src") for i in img_eles],
            "alt_text":     img_eles[0].get_attribute('alt'),
            "desc_list":    entry_ele_children_extracted,
        }

        print(f"==> DEBUG: temp_page_details = {json.dumps(temp_page_details, indent=4)}")
        if (driver.current_url != end_url):
            driver.find_element(By.LINK_TEXT, "Next >").click()
            chapter_details.append(temp_page_details)

        else:
            print(f"==> INFO: Finished scraping URLs")
            break

    return chapter_details


def get_chapter_images(chapter_dir: str, chapter_details: list):
    print(f"==> INFO: Entered get_chapter_images()")

    for page in chapter_details:
        for image in page["image_urls"]:

            image_path = f"{chapter_dir}/"
            print(f"==> INFO: Downloading image '{image}'")


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
