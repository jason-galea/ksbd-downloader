#!/usr/bin/python3

"""
Script to download the webcomic "Kill Six Billion Demons".
"""

from urllib.request import urlretrieve
from urllib.parse import urlparse
from glob import glob

import os
import sys
import json
import click

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
                # "start_url":    "https://killsixbilliondemons.com/comic/ksbd-1-8/",
                # "end_url":      "https://killsixbilliondemons.com/comic/ksbd-1-8/"
                "end_url":      "https://killsixbilliondemons.com/comic/ksbd-1-17/"
            },
            {
                "start_url":    "https://killsixbilliondemons.com/comic/ksbd-2-0/",
                # "start_url":    "https://killsixbilliondemons.com/comic/ksbd-2-34/",
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
CWD = os.getcwd()


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
    "BEGIN"


    ### Args
    if not book:
        sys.exit("==> ERROR: Please provide the number of the book to download, from 1-6")

    if not chapter:
        print("==> INFO: No chapter specified, defaulting to all chapters")
        chapters = list(range(len(BOOKS_INFO[book-1]["chapters"]))) ### [0,1,2,3,4,5]
    else:
        chapters = [chapter-1] ### [0]

    if (dont_get_details and dont_get_images):
        sys.exit("==> ERROR: You must download either page details or images, exiting early")


    ### Vars
    # DOWNLOAD_DIR = f"{CWD}/out"
    BOOK_DIR = f"{CWD}/out/{book}-{BOOKS_INFO[book-1]['name']}"

    # print(f"==> DEBUG: book = {book}")
    # print(f"==> DEBUG: chapter = {chapter}")
    # print(f"==> DEBUG: get_details = {dont_get_details}")
    # print(f"==> DEBUG: get_images = {dont_get_images}")
    # print(f"==> DEBUG: CWD = {CWD}")
    # print(f"==> DEBUG: DOWNLOAD_DIR = {DOWNLOAD_DIR}")
    # print(f"==> DEBUG: BOOK_DIR = {BOOK_DIR}")
    # print()


    ### Create dirs
    # create_dirs(DOWNLOAD_DIR)
    create_dirs(BOOK_DIR)


    ### Create webdriver
    print("==> INFO: Initialising webdriver")
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = webdriver.Firefox(
        options=driver_options,
    )


    for c in chapters:

        chapter_details_file = f"{BOOK_DIR}/{c+1}-details.json"


        ### Get details
        ### TODO: Improve logic
        if (force_get_details) and (os.path.exists(chapter_details_file)):
            print(f"==> INFO: 'force_get_details' enabled, removing '{os.path.basename(chapter_details_file)}'")
            os.remove(chapter_details_file)

        if not os.path.exists(chapter_details_file):

            if not dont_get_details:

                print(f"\n==> INFO: Begin downloading page details for book {book}, chapter {c+1}")

                chapter_details = get_chapter_details(driver, **BOOKS_INFO[book-1]["chapters"][c])
                # chapter_details = get_chapter_details(driver, BOOKS_INFO[book-1]["chapters"][c])

                print(f"==> INFO: Finished downloading page details for book {book}, chapter {c+1}")
                print(f"==> INFO: Writing chapter details to '{chapter_details_file}'")

                with open(chapter_details_file, "w", encoding="utf8") as f:
                    f.write(standard_json_dumps(chapter_details))
            else:
                print("==> INFO: Skipped downloading chapter details due to 'dont_get_details'")

        else:
            print(f"==> INFO: Detected existing chapter details file '{chapter_details_file}'")
            with open(chapter_details_file, "r", encoding="utf8") as f:
                chapter_details = json.load(f)


        # # print(f"==> DEBUG: chapter_details = {json.dumps(chapter_details, indent=4, ensure_ascii=False)}")
        # print(f"==> DEBUG: chapter_details = {standard_json_dumps(chapter_details)}")


        ### Get images
        if not dont_get_images:

            if force_get_images:
                for f in glob(f"./out/{book}-*/{c+1}-*.jpg"):
                    os.remove(f)

            ### NOTE: File must exist at this point
            with open(chapter_details_file, "r", encoding="utf8") as f:
                chapter_details = json.load(f)

            print(f"\n==> INFO: Started downloading images for book {book}, chapter {c+1}")


            get_chapter_images(BOOK_DIR, chapter_details, c)


            print(f"==> INFO: Finished downloading images for book {book}, chapter {c+1}")

        else:
            print("==> INFO: Skipped downloading images due to 'dont_get_images'")


def create_dirs(d: str) -> None:
    """
    Creates given dir + parent dirs, if they don't exist
    """

    if not os.path.exists(d):
        print(f"==> INFO: Creating directory '{d}'")
        os.makedirs(d)


def standard_json_dumps(var: any) -> str:
    """
    Returns json object, preserving ASCII characters
    """

    return json.dumps(var, indent=4, ensure_ascii=False)


def get_chapter_details(driver: webdriver.Firefox, start_url: str, end_url: str) -> list:
# def get_chapter_details(driver: webdriver.Firefox, chapter_urls: dict) -> list:
    """
    Iterates through given start/end URLs to get details of chapter
    Returns list of details, containing dictionaries for each page
    """

    driver.get(start_url)
    # driver.get(chapter_urls["start_url"])

    chapter_details = []
    while True:

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

        # img_eles = driver.find_elements(By.XPATH,
        #     "//img[contains(@src,'killsixbilliondemons.com/wp-content/uploads/')]",
        # )
        comic_ele = driver.find_element(By.ID, "comic")
        img_eles = comic_ele.find_elements(By.TAG_NAME, "img")

        temp_page_details = {
            "title":        title_ele.text,
            "image_urls":   [i.get_attribute("src") for i in img_eles],
            "alt_text":     img_eles[0].get_attribute('alt'),
            "desc_list":    entry_ele_children_extracted,
        }

        print(f"==> INFO: Downloaded details for page '{temp_page_details['title']}'")

        chapter_details.append(temp_page_details)


        if driver.current_url != end_url:
        # if driver.current_url != chapter_urls["end_url"]:
            driver.find_element(By.LINK_TEXT, "Next >").click()
        else:
            break

    return chapter_details


def get_chapter_images(d: str, chapter_details: list, chapter_no: int) -> None:
    """
    asd
    """

    for p, page in enumerate(chapter_details):
        for i, image_url in enumerate(page["image_urls"]):

            image_url_parsed = urlparse(image_url)
            original_image_file = os.path.basename(image_url_parsed.path)

            # image_file = f"{d}/{chapter_no+1}-{str(p).zfill(2)}-{original_image_file}"
            # image_file = f"{d}/c{chapter_no+1}-p{str(p).zfill(2)}-i{i}-{original_image_file}" ### "c1-p00-i0-ksbdcoverchapter1.jpg"
            image_file = f"{d}/{chapter_no+1}-{str(p).zfill(2)}-{i}-{original_image_file}" ### "1-00-0-ksbdcoverchapter1.jpg"

            if not os.path.exists(image_file):
                urlretrieve(image_url, image_file)
                print(f"==> INFO: Downloaded image '{os.path.basename(image_file)}'")

            else:
                print(f"==> INFO: Image '{os.path.basename(image_file)}' already exists")


if __name__ == "__main__":
    main() # pylint: disable=no-value-for-parameter
