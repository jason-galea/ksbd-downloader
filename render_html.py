#!/usr/bin/python3

"""
Script to render downloaded chapter details & images into an HTML document
"""

import os
import json
# import jinja2

from jinja2 import Environment, PackageLoader, select_autoescape

CWD = os.getcwd()
BOOKS_INFO_FILE = f"{CWD}/misc/book_info.json"

with open(BOOKS_INFO_FILE, "r", encoding="utf8") as book_f:
    BOOKS_INFO = json.load(book_f)

def main():
    """
    Main
    """

    book = 1
    # book_name = BOOKS_INFO[book-1]['name']
    # book_dir = f"{CWD}/out/{book}-{book_name}"
    book_dir = f"{CWD}/out/{book}-{BOOKS_INFO[book-1]['name']}"

    # chapters = list(range(len(BOOKS_INFO[book-1]["chapters"]))) ### [0,1,2,3,4,5]
    chapters = [0]

    # environment = Environment(loader=BaseLoader)
    env = Environment(
        loader=PackageLoader("ksbd_downloader"),
        autoescape=select_autoescape(),
    )

    # book_template_file = env.get_template(f"{CWD}/templates/book.html.j2")
    book_template_file = env.get_template("book.html.j2")
    
    book_result_file = f"{book_dir}.html"


    for c in chapters:

        chapter_details_file = f"{book_dir}/chapter-{c+1}-details.json"

        print(f"==> INFO: Reading chapter details file '{os.path.basename(chapter_details_file)}'")
        with open(chapter_details_file, "r", encoding="utf8") as f:
            chapter_details = json.load(f)

        
        # print(f"==> DEBUG: chapter_details[0] = {chapter_details[0]}")
        # print(f"==> DEBUG: chapter_details[0] = {json.dumps(chapter_details[0], indent=2, ensure_ascii=False)}")

        # chapter_details[0] = {
        # "page_url": "https://killsixbilliondemons.com/comic/kill-six-billion-demons-chapter-1/",
        # "title": "KILL SIX BILLION DEMONS – Chapter 1",
        # "image_urls": [
        #     "https://killsixbilliondemons.com/wp-content/uploads/2013/04/ksbdcoverchapter1.jpg"
        # ],
        # "alt_text": "KILL SIX BILLION DEMONS – Chapter 1",
        # "desc_list": [
        #     "“Let there be no Genesis, for beginnings are false and I am a consummate liar.”",
        #     "-Psalms"
        # ]
        # }

        # context = {
        #     "students": students,
        #     "test_name": test_name,
        #     "max_score": max_score,
        # }

        book_result_rendered = book_template_file.render(
            chapter_no=c+1,
            **chapter_details[0]
            # {
            #     "image_urls":   chapter_details[0]["image_urls"],
            #     "title":        chapter_details[0]["title"],
            #     "chapter_no":   c+1,
            #     "alt_text":     chapter_details[0]["alt_text"]
            # }
        )

        with open(book_result_file, mode="w", encoding="utf-8") as results:
            results.write(book_result_rendered)

            print(f"==> INFO: Wrote '{os.path.basename(book_result_file)}'")


if __name__ == "__main__":
    # main() # pylint: disable=no-value-for-parameter
    main()
