# ksbd-downloader
Scripts to download webcomic "Kill Six Billion Demons".

This script uses Selenium to fetch image URLs from "https://killsixbilliondemons.com", then download them.

# Features
- Detect existing images from previous runs
- Detect existing image URLs from previous runs

# Using the script

Statically set "FIRST_COMIC" and "LAST_COMIC" variables with relevant URLs.

Then, simply execute from the base repository dir:

    ./ksbd-downloader.py
