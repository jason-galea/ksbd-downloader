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
    book_dir_relative_to_result_file = f"./{book}-{BOOKS_INFO[book-1]['name']}"

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

        # {
        #     "title": "KILL SIX BILLION DEMONS – Chapter 1",
        #     "image_dict": {
        #         "1-00-0-ksbdcoverchapter1.jpg": "https://killsixbilliondemons.com/wp-content/uploads/2013/04/ksbdcoverchapter1.jpg"
        #     },
        #     "page_url": "https://killsixbilliondemons.com/comic/kill-six-billion-demons-chapter-1/",
        #     "alt_text": "KILL SIX BILLION DEMONS – Chapter 1",
        #     "desc_dict": {
        #         "p": "-Psalms"
        #     }
        # },

        book_result_rendered = book_template_file.render(
            book=book,
            book_title=BOOKS_INFO[book-1]['title'],
            book_dir=book_dir_relative_to_result_file,
            # chapter_no=c+1,
            # **chapter_details[0]
            chapter_details=chapter_details,
        )

        with open(book_result_file, mode="w", encoding="utf-8") as results:
            results.write(book_result_rendered)

            print(f"==> INFO: Wrote '{os.path.basename(book_result_file)}'")


if __name__ == "__main__":
    # main() # pylint: disable=no-value-for-parameter
    main()
