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

from books_info import BOOKS_INFO


### Globals
CWD = os.getcwd()


@click.command()
@click.option("-b", "--book", type=int, help="Book # to download, from 1-6.")
@click.option("-c", "--chapter", type=int, help="Chapter # to download. Defaults to downloading all chapters")
@click.option("-od", "--only_details", is_flag=True, help="Only download images, assuming image URLs are known")
@click.option("-oi", "--only_images", is_flag=True, help="Only download page details, ignoring images")
@click.option("-fgd", "--force_get_details", is_flag=True, help="Ignore previously downloaded details")
@click.option("-fgi", "--force_get_images", is_flag=True, help="Ignore previously downloaded images")
def main(
    book: int,
    chapter: int,
    only_images: bool,
    only_details: bool,
    force_get_details: bool,
    force_get_images: bool
):
    """
    Main function
    """

    if not book:
        sys.exit("==> ERROR: Book number must be specified")

    if (only_images and only_details):
        sys.exit("==> ERROR: You must download either page details or images")

    chapters_info = BOOKS_INFO[book-1]["chapters"]
    book_dir = f"{CWD}/out/{book}-{BOOKS_INFO[book-1]['name']}"

    if chapter:
        chapters = [chapter-1] ### [0]
    else:
        print("==> INFO: No chapter specified, defaulting to all chapters")
        chapters = list(range(len(chapters_info))) ### [0,1,2,3,4,5]

    # print(f"==> DEBUG: book = {book}")
    # print(f"==> DEBUG: chapter = {chapter}")
    # print(f"==> DEBUG: get_details = {only_images}")
    # print(f"==> DEBUG: get_images = {only_details}")
    # print(f"==> DEBUG: CWD = {CWD}")
    # print(f"==> DEBUG: DOWNLOAD_DIR = {DOWNLOAD_DIR}")
    # print(f"==> DEBUG: book_dir = {book_dir}")
    # print()

    # create_dirs(DOWNLOAD_DIR)
    create_dirs(book_dir)

    print("==> INFO: Initialising webdriver")
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = webdriver.Firefox(
        options=driver_options,
    )

    for c in chapters:
        chapter_details_file = f"{book_dir}/chapter-{c+1}-details.json"
        start_url, end_url = chapters_info[c]


        ### Get details
        ### TODO: Improve logic
        if (force_get_details) and (os.path.exists(chapter_details_file)):
            print(f"==> INFO: 'force_get_details' enabled, removing '{os.path.basename(chapter_details_file)}'")
            os.remove(chapter_details_file)

        if not os.path.exists(chapter_details_file):

            if not only_images:

                print(f"\n==> INFO: Begin downloading page details for book {book}, chapter {c+1}")
                chapter_details = get_chapter_details(
                    driver=driver,
                    start_url=start_url,
                    end_url=end_url,
                    chapter=c,
                )
                print(f"==> INFO: Finished downloading page details for book {book}, chapter {c+1}")

                print(f"==> INFO: Writing chapter details to '{chapter_details_file}'")
                with open(chapter_details_file, "w", encoding="utf8") as f:
                    f.write(standard_json_dumps(chapter_details))

            else:
                print("==> INFO: Skipped downloading chapter details due to 'only_images'")

        else:
            print(f"==> INFO: Detected existing chapter details file '{chapter_details_file}'")
            with open(chapter_details_file, "r", encoding="utf8") as f:
                chapter_details = json.load(f)


        # # print(f"==> DEBUG: chapter_details = {json.dumps(chapter_details, indent=4, ensure_ascii=False)}")
        # print(f"==> DEBUG: chapter_details = {standard_json_dumps(chapter_details)}")


        ### Get images
        if not only_details:

            if force_get_images:
                for f in glob(f"./out/{book}-*/{c+1}-*.jpg"):
                    os.remove(f)

            ### NOTE: File must exist at this point
            with open(chapter_details_file, "r", encoding="utf8") as f:
                chapter_details = json.load(f)

            get_chapter_images(book, book_dir, chapter_details, c)

        else:
            print("==> INFO: Skipped downloading images due to 'only_details'")


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


def get_chapter_details(
    driver: webdriver.Firefox,
    chapter: int,
    start_url: str,
    end_url: str,
) -> list:
    """
    Iterates through given start/end URLs to get details of chapter

    Returns list of details, containing dictionaries for each page
    """


    ### DOWNLOAD
    driver.get(start_url)

    page_no = 0
    chapter_details = []
    while True:

        title_ele = driver.find_element(By.CLASS_NAME, "post-title")


        ### Description
        entry_ele = driver.find_element(By.CLASS_NAME, "entry")
        entry_ele_children = entry_ele.find_elements(By.CSS_SELECTOR, "*")

        desc_list = []
        for e in entry_ele_children:

            temp_src = temp_text = None

            if (e.tag_name == "p") and not (e.find_elements(By.TAG_NAME, "a")):
                ### NOTE: Ignore paragraphs with children
                temp_text = e.text
            elif e.tag_name == "img":
                temp_src = e.get_attribute("src")
            elif (e.tag_name == "a") and ("title" in e.__dict__.keys()):
                ### TODO: Find what page this applies to?
                temp_text = e.title
            elif e.tag_name == "a":
                temp_src = e.get_attribute("href")
                temp_text = e.text

            if (temp_src) or (temp_text):
                desc_list.append({
                    "type":     e.tag_name,
                    "src":      temp_src,
                    "text":     temp_text
                })


        ### Image filenames & URLs
        comic_ele = driver.find_element(By.ID, "comic")
        image_eles = comic_ele.find_elements(By.TAG_NAME, "img")
        image_urls = [i.get_attribute("src") for i in image_eles]
        # image_urls = [i.get_attribute("src") for i in comic_ele.find_elements(By.TAG_NAME, "img")]

        image_dict = {}
        for i, image_url in enumerate(image_urls):

            image_url_parsed = urlparse(image_url)
            original_image_file = os.path.basename(image_url_parsed.path)

            ### "c1-p00-i0-ksbdcoverchapter1.jpg"
            # image_file = f"{book_dir}/c{chapter+1}-p{str(page_no).zfill(2)}-i{i}-{original_image_file}"
            ### "1-00-0-ksbdcoverchapter1.jpg"
            image_file = f"{chapter+1}-{str(page_no).zfill(2)}-{i}-{original_image_file}"

            image_dict.update({image_file: image_url})


        temp_page_details = {
            "title":            title_ele.text,
            "image_dict":       image_dict,
            "page_url":         driver.current_url,
            "alt_text":         image_eles[0].get_attribute('alt'),
            # "desc_list":        entry_ele_children_extracted,
            "desc_list":        desc_list,
        }

        print(f"==> INFO: Downloaded details for page '{temp_page_details['title']}'")

        chapter_details.append(temp_page_details)

        if driver.current_url != end_url:
            driver.find_element(By.LINK_TEXT, "Next >").click()
            page_no += 1
        else:
            break

    return chapter_details


def get_chapter_images(
    book: int,
    book_dir: str,
    chapter_details: list,
    chapter: int,
) -> None:
    """
    Downloads images :o
    """

    print(f"\n==> INFO: Started downloading images for book {book}, chapter {chapter+1}")

    for page in chapter_details:
        for image_file, image_url in page["image_dict"].items():

            image_file_full_path = f"{book_dir}/{image_file}"

            if not os.path.exists(image_file_full_path):
                urlretrieve(image_url, image_file_full_path)
                print(f"==> INFO: Downloaded image '{os.path.basename(image_file)}'")

            else:
                print(f"==> INFO: Image '{os.path.basename(image_file)}' already exists")

    print(f"==> INFO: Finished downloading images for book {book}, chapter {chapter+1}")


if __name__ == "__main__":
    main() # pylint: disable=no-value-for-parameter
