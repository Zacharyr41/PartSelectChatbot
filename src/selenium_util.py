from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

from enum import Enum
from typing import Optional
import constants as cts


class PageType(Enum):
    RESULTS = 1
    PRODUCT = 2


def get_driver():
    # Check if running on Heroku
    if "DYNO" in os.environ:
        # Path settings for Heroku
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        driver = webdriver.Chrome(options=chrome_options)
    else:
        # Local settings
        # Make sure to have chromedriver in your PATH or specify the path to the executable
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    return driver


def navigate_to_url(driver, url=cts.PART_SELECT_URL):
    try:
        driver.get(url)
        time.sleep(2)
    except:
        return False
    return True


def perform_search(driver, search_term):
    try:
        search_input = driver.find_element(By.ID, "searchboxInput")
        search_input.send_keys(search_term)
        search_button = driver.find_element(By.CLASS_NAME, "btn--teal")
        search_button.click()
        time.sleep(4)
    except:
        return False

    return True


def determine_page_type(driver) -> PageType:
    main_divs = driver.find_elements(By.ID, "main")
    data_page_name = None
    if len(main_divs) > 0:
        main_div = main_divs[0]
        data_page_name = main_div.get_attribute("data-page-name")

    if data_page_name:
        return PageType.PRODUCT

    return PageType.RESULTS


def extract_links_from_results(driver):
    try:
        result_links = driver.find_elements(
            By.CSS_SELECTOR, ".nf__part__detail__title")
        num_urls = min(3, len(result_links))
        urls = [link.get_attribute('href') for link in result_links[:num_urls]]
    except:
        return []

    return urls


def extract_data_from_product_page(driver, url : Optional[str] = None):
    if url:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
    all_text = driver.execute_script("return document.body.innerText;")
    split_top_off = all_text.split('customerservice@partselect.com')
    if len(split_top_off) > 1:
        relevant_text = split_top_off[1]
        return relevant_text
    return all_text


