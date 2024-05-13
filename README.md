# ksbd-downloader
Scripts to download & display the webcomic "Kill Six Billion Demons".

`ksbd_downloader.py` downloads page details & images, including:
- Title
- Image URL(s)
- Alt text
- Page description text (including secondary images!)

`render_chapter_html.py` can then transform the downloaded files into readable HTML


<!-- # Features
- Detect existing images from previous runs
- Detect existing image URLs from previous runs -->


## Downloader - Help
    $ ./ksbd_downloader.py --help
    Usage: ksbd_downloader.py [OPTIONS]

      Main function

    Options:
      -b, --book INTEGER         Book # to download, from 1-6.
      -c, --chapter INTEGER      Chapter # to download. Defaults to downloading
                                 all chapters
      -od, --only_details        Only download images, assuming image URLs are
                                 known
      -oi, --only_images         Only download page details, ignoring images
      -fgd, --force_get_details  Ignore previously downloaded details
      -fgi, --force_get_images   Ignore previously downloaded images
      --help                     Show this message and exit.


## Downloader - Examples:
Download book 1 (all chapters)

    ./ksbd_downloader.py -b 1

Download book 1, chapter 5

    ./ksbd_downloader.py -b 1 -c 5

Download book 1, chapter 5, and ignore previously downloaded chapter details

    ./ksbd_downloader.py -b 1 -c 5 --force_get_details

Download book 3 (all chapters) chapter details only, no images

    ./ksbd_downloader.py -b 3 --only_details

Etc.


<!-- ## HTML Renderer - Help -->
<!-- TODO: Use click for CMD args & add help text here -->


## HTML Renderer - Examples
asd

    render_chapter_html.py -b 1 -c 1


## TODO:
- Async downloads
- Detect if image exists, handle --force_get_images
- Improve get_details() logic for --force_get_details & existing files
- Add instructions for `render_html.py`
- Add book & chapter CLI options for `render_chapter_html.py`
- Use single `<div class="columns is-mobile is-centered">` element
- Convert static HTML to Flask, with home pages for books & chapters


<!-- # What do I do with all these images?
The images are downloaded with a zero-filled page number prefix, meaning you can simply ZIP them into a functional CBZ file for your favourite comic book reader. Cool!  -->
