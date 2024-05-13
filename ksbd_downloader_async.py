#!/usr/bin/python3

from urllib.request import urlretrieve
from urllib.parse import urlparse
from glob import glob
import os
import json
import click
# import urllib
# import pickle
# import argparse
import httpx
import asyncio
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

from books_info import BOOKS_INFO


### Globals
GET_IMAGE_WORKER_COUNT = 4


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
        chapters = list(range(len(BOOKS_INFO[book-1]["chapters"]))) ### [0,1,2,3,4,5]
    else:
        chapters = [chapter-1] ### [0]

    if (dont_get_details and dont_get_images):
        exit(f"==> ERROR: You must download either page details or images, exiting early")


    ### Vars
    CWD = os.getcwd()
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

                print(f"==> INFO: Finished downloading page details for book {book}, chapter {c+1}")
                print(f"==> INFO: Writing chapter details to '{chapter_details_file}'")

                with open(chapter_details_file, "w", encoding="utf8") as f:
                    f.write(standard_json_dumps(chapter_details))
            else:
                print(f"==> INFO: Skipped downloading chapter details due to 'dont_get_details'")

        else:
            print(f"==> INFO: Detected existing chapter details file '{chapter_details_file}'")
            with open(chapter_details_file, "r", encoding="utf8") as f:
                chapter_details = json.load(f)


        # if (force_get_details) and (os.path.exists(chapter_details_file)):
        #     print(f"==> INFO: 'force_get_details' enabled, removing '{os.path.basename(chapter_details_file)}'")
        #     os.remove(chapter_details_file)

        # if not dont_get_details:

        #     if (not os.path.exists(chapter_details_file)) or (force_get_details):
        #         print(f"\n==> INFO: Begin downloading page details for book {book}, chapter {c+1}")

        #         chapter_details = get_chapter_details(driver, **BOOKS_INFO[book-1]["chapters"][c])

        #         print(f"==> INFO: Finished downloading page details for book {book}, chapter {c+1}")
        #         print(f"==> INFO: Writing chapter details to '{chapter_details_file}'")

        #         with open(chapter_details_file, "w", encoding="utf8") as f:
        #             f.write(standard_json_dumps(chapter_details))

        #     elif not force_get_details:


        #     else:
        #         print(f"==> INFO: Chapter details file '{chapter_details_file}' already exists")


        # else:
        #     print(f"==> INFO: Skipped downloading chapter details due to 'dont_get_details'")


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
            # asyncio.run(get_chapter_images_async(BOOK_DIR, chapter_details, c))


            # ##################################################################
            # ### PROFILING
            # import cProfile
            # import pstats

            # with cProfile.Profile() as pr:
            #     # get_chapter_images(BOOK_DIR, chapter_details, c)
            #     get_chapter_images_async(BOOK_DIR, chapter_details, c)

            # stats = pstats.Stats(pr)
            # stats.sort_stats(pstats.SortKey.TIME)
            # stats.print_stats()
            # ### PROFILING
            # ##################################################################


            print(f"==> INFO: Finished downloading images for book {book}, chapter {c+1}")

        else:
            print(f"==> INFO: Skipped downloading images due to 'dont_get_images'")


def create_dirs(dir_path: str) -> None:
    if not (os.path.exists(dir_path)):
        print(f"==> INFO: Creating directory '{dir_path}'")
        os.makedirs(dir_path)


def standard_json_dumps(var: any) -> str:
    return json.dumps(var, indent=4, ensure_ascii=False)


def get_chapter_details(driver: webdriver.Firefox, start_url: str, end_url: str) -> list:

    driver.get(start_url)

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


        if (driver.current_url != end_url):
            driver.find_element(By.LINK_TEXT, "Next >").click()
        else:
            break

    return chapter_details


# async def get_chapter_images_async(dir: str, chapter_details: list, chapter_no: int) -> None:

#     queue = asyncio.Queue()
#     existing_images = glob(f"{dir}/{chapter_no+1}-*.jpg")


#     async with httpx.AsyncClient() as client:

#         tasks = []

#         ### Generate work items (data required for a worker to know how to perform a task)
#         for p, page in enumerate(chapter_details):
#             for i, image_url in enumerate(page["image_urls"]):

#                 image_url_parsed = urlparse(image_url)
#                 original_image_file = os.path.basename(image_url_parsed.path)

#                 # image_file = f"{dir}/{chapter_no+1}-{str(p).zfill(2)}-{original_image_file}"
#                 # image_file = f"{dir}/c{chapter_no+1}-p{str(p).zfill(2)}-i{i}-{original_image_file}" ### "c1-p00-i0-ksbdcoverchapter1.jpg"
#                 image_file = f"{dir}/{chapter_no+1}-{str(p).zfill(2)}-{i}-{original_image_file}" ### "1-00-0-ksbdcoverchapter1.jpg"

#                 # if not os.path.exists(image_file):
#                 if not image_file in existing_images:
#                     # queue.put_nowait(urlretrieve(image_url, image_file))
#                     queue.put_nowait((image_url, image_file))

#                 #     print(f"==> INFO: Downloaded image '{os.path.basename(image_file)}'")
#                 # else:
#                 #     print(f"==> INFO: Image '{os.path.basename(image_file)}' already exists")


#         ### Create worker tasks
#         # tasks = [asyncio.create_task(get_chapter_images_worker(i)) for i in range(GET_IMAGE_WORKER_COUNT)]
#         tasks = [asyncio.create_task(get_chapter_images_worker(queue, client)) for _ in range(GET_IMAGE_WORKER_COUNT)]

#         ### Wait until queue is processed
#         await queue.join()

#         ### Cancel worker tasks
#         for task in tasks:
#             task.cancel()

#         ### Wait for all worker tasks to be cancelled
#         await asyncio.gather(*tasks, return_exceptions=True)


# async def get_chapter_images_worker(queue: asyncio.Queue, client: httpx.AsyncClient):
#     while True:

#         ### Get a "work item" from queue
#         url_file_tuple = await queue.get()
#         url = url_file_tuple[0]
#         file = url_file_tuple[1]

#         ### Execute the work
#         # urlretrieve(*url_file_tuple) ### E.G: urlretrieve(url_file_tuple[0], url_file_tuple[1])
#         image_response = client.get(url)
#         with open(file) as f:
#             f.write(image_response.content)

#         ### Notify queue
#         queue.task_done()

#         print(f"==> INFO: Downloaded image '{os.path.basename(url_file_tuple[1])}'")


# async def get_chapter_images_async(dir: str, chapter_details: list, chapter_no: int) -> None:

#     queue = asyncio.Queue()
#     existing_images = glob(f"{dir}/{chapter_no+1}-*.jpg")

#     ### Generate work items (data required for a worker to know how to perform a task)
#     for p, page in enumerate(chapter_details):
#         for i, image_url in enumerate(page["image_urls"]):

#             image_url_parsed = urlparse(image_url)
#             original_image_file = os.path.basename(image_url_parsed.path)

#             # image_file = f"{dir}/{chapter_no+1}-{str(p).zfill(2)}-{original_image_file}"
#             # image_file = f"{dir}/c{chapter_no+1}-p{str(p).zfill(2)}-i{i}-{original_image_file}" ### "c1-p00-i0-ksbdcoverchapter1.jpg"
#             image_file = f"{dir}/{chapter_no+1}-{str(p).zfill(2)}-{i}-{original_image_file}" ### "1-00-0-ksbdcoverchapter1.jpg"

#             # if not os.path.exists(image_file):
#             if not image_file in existing_images:
#                 # queue.put_nowait(urlretrieve(image_url, image_file))
#                 queue.put_nowait((image_url, image_file))

#             #     print(f"==> INFO: Downloaded image '{os.path.basename(image_file)}'")
#             # else:
#             #     print(f"==> INFO: Image '{os.path.basename(image_file)}' already exists")

#     async with httpx.AsyncClient() as client:

#         ### Create worker tasks
#         # tasks = [asyncio.create_task(get_chapter_images_worker(i)) for i in range(GET_IMAGE_WORKER_COUNT)]
#         tasks = [asyncio.create_task(get_chapter_images_worker(queue, client)) for _ in range(GET_IMAGE_WORKER_COUNT)]

#         ### Wait until queue is processed
#         await queue.join()

#         ### Cancel worker tasks
#         for task in tasks:
#             task.cancel()

#         ### Wait for all worker tasks to be cancelled
#         await asyncio.gather(*tasks, return_exceptions=True)


# async def get_chapter_images_worker(queue: asyncio.Queue, client: httpx.AsyncClient):
#     while True:

#         ### Get a "work item" from queue
#         url_file_tuple = await queue.get()
#         url = url_file_tuple[0]
#         file = url_file_tuple[0]

#         ### Execute the work
#         # urlretrieve(*url_file_tuple) ### E.G: urlretrieve(url_file_tuple[0], url_file_tuple[1])
#         image_response = client.get(url)
#         with open(file) as f:
#             f.write(image_response.content)

#         ### Notify queue
#         queue.task_done()

#         print(f"==> INFO: Downloaded image '{os.path.basename(url_file_tuple[1])}'")



def get_chapter_images(dir: str, chapter_details: list, chapter_no: int) -> None:
    for p, page in enumerate(chapter_details):
        for i, image_url in enumerate(page["image_urls"]):

            image_url_parsed = urlparse(image_url)
            original_image_file = os.path.basename(image_url_parsed.path)

            # image_file = f"{dir}/{chapter_no+1}-{str(p).zfill(2)}-{original_image_file}"
            # image_file = f"{dir}/c{chapter_no+1}-p{str(p).zfill(2)}-i{i}-{original_image_file}" ### "c1-p00-i0-ksbdcoverchapter1.jpg"
            image_file = f"{dir}/{chapter_no+1}-{str(p).zfill(2)}-{i}-{original_image_file}" ### "1-00-0-ksbdcoverchapter1.jpg"

            if not os.path.exists(image_file):
                urlretrieve(image_url, image_file)
                print(f"==> INFO: Downloaded image '{os.path.basename(image_file)}'")

            else:
                print(f"==> INFO: Image '{os.path.basename(image_file)}' already exists")


if (__name__ == "__main__"):
    main()


    # import cProfile
    # import pstats

    # with cProfile.Profile() as pr:
    #     main()

    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
