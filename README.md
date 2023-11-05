# ksbd-downloader
Script to download the webcomic "Kill Six Billion Demons".

The script first downloads the details of each page, including:
- Title
- Image URL(s)
- Alt text
- Page description text (including images!)

Then, images are downloaded asynchronously from the above image URLs


<!-- # Features
- Detect existing images from previous runs
- Detect existing image URLs from previous runs -->


## Using the script
    ./ksbd_downloader.py --help

    Usage: ksbd_downloader.py [OPTIONS]

    Options:
        -b, --book INTEGER     Book # to download, from 1-6.
        -c, --chapter INTEGER  Chapter # to download. Defaults to downloading all
                                chapters
        --dont_get_details     Only download page details, ignoring images
        --dont_get_images      Only download images, assuming image URLs are known
        --force_get_details    Ignore previously downloaded details
        --force_get_images     Ignore previously downloaded images
        --help                 Show this message and exit.


## Examples:
Download book 1 (all chapters)

    ./ksbd_downloader.py -b 1
    
Download book 1, chapter 5

    ./ksbd_downloader.py -b 1 -c 5
    
Download book 1, chapter 5, and ignore previously downloaded chapter details

    ./ksbd_downloader.py -b 1 -c 5 --force_get_details
    
Download book 3 (all chapters) chapter details only, no images

    ./ksbd_downloader.py -b 3 --dont_get_images

Etc.


## TODO:
- Async downloads
- Detect if image exists, handle --force_get_images
- Improve get_details() logic for --force_get_details & existing files
- Add instructions for `render_html.py`
- Add book & chapter CLI options for `render_html.py`
- Handle "FULL SIZE" anchors in descriptions
- Use single `<div class="columns is-mobile is-centered">` element


<!-- # What do I do with all these images?
The images are downloaded with a zero-filled page number prefix, meaning you can simply ZIP them into a functional CBZ file for your favourite comic book reader. Cool!  -->
