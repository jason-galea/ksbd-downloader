#!/usr/bin/python3

import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


#########################################################################################
### Globals
TEST_URL = "https://killsixbilliondemons.com/comic/breaker-of-infinities-1-9-to-1-10/"


#########################################################################################
def main():

    ### Init
    print("==> Initialising driver")
    driver_options = Options()
    driver_options.add_argument("--headless")
    driver = webdriver.Firefox(
        options=driver_options,
    )

    print(f"==> Loading '{TEST_URL}'")
    driver.get(TEST_URL)
    


    # print(f"==> Finding 'comic' div")
    # comic_div_element = driver.find_element(By.ID, "comic")
    # # comic_div_element = driver.find_element(By.XPATH, "//div[@id='comic']*img//")
    # # comic_div_element = driver.find_element(By.XPATH, "//div[@id='comic']//img")
    # print(comic_div_element)
    
    # img = driver.find_element(By.XPATH, "//div[@id='comic']/img")
    # print(img)

    # imgs = driver.find_elements(By.XPATH, "//div[@id='comic']*img")
    imgs = driver.find_elements(
        By.XPATH,
        "//img[starts-with(@src,'https://killsixbilliondemons.com/wp-content/uploads/')]",
    )
    print(imgs)


if (__name__ == "__main__"):
    main()
