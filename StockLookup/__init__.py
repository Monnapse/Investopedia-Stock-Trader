"""
    StockLookup
    Made by Monnapse
    Lookup stock info using yahoo finance
"""

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from enum import Enum

wait_time = 20
yahoo_base_urls = [
    "https://query1.finance.yahoo.com", "https://query2.finance.yahoo.com"
]
lookup_url = "/v8/finance/chart/%s?period1=%s&period2=%s"

# DRIVER
options = Options() 
#options.headless = True
#options.add_argument("--headless=new")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options) 
web_driver_waiter = WebDriverWait(driver, wait_time)

def new_page(url: str):
        driver.get(base_url + url)

        time.sleep(1) # Wait for page to be loaded

def get_stock(symbol):
    """
        Gets just the basic info about the stock
    """
    new_page(ticker_lookup+symbol)

    return {
        "last_price": web_driver_waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'fin-streamer[data-field="regularMarketPrice"]'))).text
    }