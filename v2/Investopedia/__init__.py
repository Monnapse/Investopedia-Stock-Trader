"""
    Investopedia API
    Made by Monnapse
"""

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import time
from enum import Enum

# DRIVER
options = Options() 
#options.headless = True
#options.add_argument("--headless=new")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options) 

class Duration(Enum):
    day_only = 1
    good_until_cancel = 2

class OrderType(Enum):
    limit = 1
    market = 2
    stop_limit = 3

class Action(Enum):
    buy = 1
    sell = 2

class Account:
    def __init__(self, username: str, password:str):
        """
            Logs into Investopedia Account
        """

        self.base_url = "https://www.investopedia.com"
        self.portfolio_url = "/simulator/portfolio"

        self.new_page(self.portfolio_url)

        # Sign in
        username_element = driver.find_element(By.ID, "username")
        username_element.send_keys(username)

        password_element = driver.find_element(By.ID, "password")
        password_element.send_keys(password)

        login_element = driver.find_element(By.ID, "login")
        login_element.click()

    def new_page(self, url: str):
        driver.get(self.base_url + url)

        time.sleep(5) # Wait for page to be loaded

    def get_account_overview(self):
        """
            Gets Accounts Value, Buying Power, and Cash
        """
        self.new_page(self.portfolio_url)
        
        return {
            "account_value": driver.find_element(By.CSS_SELECTOR, 'div[data-cy="account-value-text"]').text,
            "buying_power": driver.find_element(By.CSS_SELECTOR, 'div[data-cy="buying-power-text"]').text,
            "cash": driver.find_element(By.CSS_SELECTOR, 'div[data-cy="cash-text"]').text
        }
    
    #def get_stocks
    def trade(self, symbol: str, action, quantity: int, order_type, price=0, duration=0):
        """
            Buys stock
        """

        self.new_page("/simulator/trade/stocks")

        symbol_input = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Look up Symbol/Company Name"]')
        symbol_input.send_keys(symbol)

        time.sleep(2)

        symbols_list = driver.find_element(By.CLASS_NAME, "v-select-list")
        first_stock = symbols_list.find_element(By.XPATH, "//div")
        
        #first_stock = driver.find_element(By.ID, "list-item-308-0")
        if not first_stock:
            print(f"Could not find symbol {symbol}")
            return None
        
        return first_stock

