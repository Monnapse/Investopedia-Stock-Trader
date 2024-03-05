"""
    Investopedia API
    Made by Monnapse
"""

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
import time

# DRIVER
options = Options() 
#options.headless = True
#options.add_argument("--headless=new")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options) 

class Account:
    def __init__(self, username: str, password:str):
        """
            Logs into Investopedia Account
        """

        self.base_url = "https://www.investopedia.com"
        self.portfolio_url = "/simulator/portfolio"

        self.new_page(self.portfolio_url)

        # Sign in
        usernameElement = driver.find_element(By.ID, "username")
        usernameElement.send_keys(username)

        passwordElement = driver.find_element(By.ID, "password")
        passwordElement.send_keys(password)

        loginElement = driver.find_element(By.ID, "login")
        loginElement.click()

    def new_page(self, url):
        driver.get(self.base_url + url)

        time.sleep(5) # Wait for page to be loaded

    def get_account_overview(self):
        self.new_page(self.portfolio_url)

        return driver.find_element(By.CSS_SELECTOR, 'div[data-cy="account-value-text"]').text