"""
    Investopedia API
    Made by Monnapse
"""

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from enum import Enum

wait_time = 20

# DRIVER
options = Options() 

#options.headless = True
#options.add_argument("--headless=new")

options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options) 
web_driver_waiter = WebDriverWait(driver, wait_time)

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
        username_element = web_driver_waiter.until(EC.presence_of_element_located((By.ID, 'username')))#driver.find_element(By.ID, "username")
        username_element.send_keys(username)

        password_element = web_driver_waiter.until(EC.presence_of_element_located((By.ID, 'password')))#driver.find_element(By.ID, "password")
        password_element.send_keys(password)

        login_element = web_driver_waiter.until(EC.presence_of_element_located((By.ID, 'login')))#driver.find_element(By.ID, "login")
        login_element.click()

        time.sleep(1)
        try:
            if driver.find_element(By.CLASS_NAME, "alert-error"):
                # Restart
                print("Could not login now restarting")
                self.__init__(username, password)
        except:
            pass

    def new_page(self, url: str):
        driver.get(self.base_url + url)

        time.sleep(1) # Wait for page to be loaded

    def get_account_overview(self):
        """
            Gets Accounts Value, Buying Power, and Cash
        """
        
        self.new_page(self.portfolio_url)
        
        return {
            "account_value": web_driver_waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-cy="account-value-text"]'))).text, #driver.find_element(By.CSS_SELECTOR, 'div[data-cy="account-value-text"]').text,
            "buying_power": web_driver_waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-cy="buying-power-text"]'))).text,#driver.find_element(By.CSS_SELECTOR, 'div[data-cy="buying-power-text"]').text,
            "cash": web_driver_waiter.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-cy="cash-text"]'))).text#driver.find_element(By.CSS_SELECTOR, 'div[data-cy="cash-text"]').text
        }
    
    def change_game_session(self, session_name: str):
        #data-cy="portfolio-select"
        #self.new_page("/simulator/trade/stocks")
        web_driver_waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-cy="portfolio-select"]'))).click()
        #/html/body/div[1]/div/div/div[2]/main/div/div[1]/div/div[1]/div[2]/div/div/div/div
        list = web_driver_waiter.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[1]/div/div[5]/div/div/div/div')))
        try:
            session = list.find_element(By.XPATH, f"//*[contains(text(), '{session_name}')]")
            session.click()
        except:
            pass

    #def get_stocks
    def trade(self, symbol: str, action: Action, quantity: int, order_type: OrderType=OrderType.market, price=0, duration:Duration=Duration.day_only):
        """
            Buys stock
        """

        self.new_page("/simulator/trade/stocks")

        # SYMBOL
        symbol_input = web_driver_waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Look up Symbol/Company Name"]')))#driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Look up Symbol/Company Name"]')
        symbol_input.send_keys(symbol)
       # time.sleep(2)
        symbols_list = web_driver_waiter.until(EC.visibility_of_element_located((By.CLASS_NAME, 'v-select-list')))#driver.find_element(By.CLASS_NAME, "v-select-list")
        first_stock = symbols_list.find_element(By.XPATH, "div[1]")

        #first_stock = driver.find_element(By.ID, "list-item-308-0")
        if not first_stock:
            print(f"Could not find symbol {symbol}")
            return None
        
        first_stock.click()

        # ACTION
        #action_input = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[3]/div[2]/div[2]/div[1]/div[2]/form/div[1]/div/div[1]/div/div/div[1]').click()
        web_driver_waiter.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/main/div/div[3]/div[2]/div[2]/div[1]/div[2]/form/div[1]/div/div[1]/div/div/div[1]'))).click()
        #action_list = web_driver_waiter.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[1]/main/div/div[3]/div[2]/div[2]/div[1]/div[2]/form/div[1]/div/div[1]/div/div[2]/div')))
        if action.value == 1:
            # Buying
            #driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[4]/div/div[1]').click()
            web_driver_waiter.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[1]'))).click()
        elif action.value == 2:
            # Selling
            #driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[4]/div/div[2]').click()
            print("selling")
            web_driver_waiter.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div[2]'))).click()

        # QUANTITY
        quantity_input = web_driver_waiter.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[role="select-quantity"]')))#driver.find_element(By.CSS_SELECTOR, 'input[role="select-quantity"]')
        quantity_input.send_keys(quantity)

        # Order Type
        #order_type_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div[3]/div[2]/div[2]/div[1]/div[2]/form/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]').click()
        #web_driver_waiter.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/main/div/div[3]/div[2]/div[2]/div[1]/div[2]/form/div[2]/div/div[1]/div/div/div[1]/div[1]/div[1]'))).click()
        #if order_type.value == 1:
        #    #driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[5]/div/div[1]").click()
        #    web_driver_waiter.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[5]/div/div[1]'))).click()
        #elif order_type.value == 2:
        #    #driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[5]/div/div[2]").click()
        #    web_driver_waiter.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[5]/div/div[2]'))).click()
        #elif order_type.value == 3:
        #    #driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[5]/div/div[3]").click()
        #    web_driver_waiter.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[5]/div/div[3]'))).click()

        # Duration
        #duration_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div[3]/div[2]/div[2]/div[1]/div[2]/form/div[2]/div/div[2]/div/div/div[1]/div[1]').click()
        #if duration.value == 1:
        #    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[6]/div/div[1]").click()
        #elif duration.value == 2:
        #    driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[6]/div/div[2]").click()
            
        # Price
        #if order_type.value != 2:
        #    price_input = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[1]/main/div/div[2]/div[2]/div[2]/div[1]/div[2]/form/div[2]/div/div[2]/div/div/div/div[1]/div/input")
        #    if price_input:
        #        price_input.send_keys(price)

        # Preview Order
        #time.sleep(5)
        # driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div[3]/div[2]/div[2]/div[1]/div[2]/form/div[3]/div/div[2]/button').click()
        #
        # time.sleep(2)
        preview_button = web_driver_waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-cy="preview-button"]')))
        #preview_button.click()
        driver.execute_script("arguments[0].click()", preview_button)

        time.sleep(1)
        try:
            if driver.find_element(By.CSS_SELECTOR, 'li[data-cy="stock-trade-error"]'):
                return None, driver.find_element(By.CSS_SELECTOR, 'li[data-cy="stock-trade-error"]').text
        except:
            pass

        # Submit Order
        web_driver_waiter.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-cy="submit-order-button"]'))).click()

        #driver.find_element(By.LINK_TEXT, '/html/body/div[1]/div/div/div[3]/div/div/div[3]/div/div/div[2]').click()

        print(f"Successfully traded {quantity} {symbol} stocks")