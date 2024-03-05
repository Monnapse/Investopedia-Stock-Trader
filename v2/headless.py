from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
  
# instance of Options class allows 
# us to configure Headless Chrome 
options = Options() 
  
# this parameter tells Chrome that 
# it should be run without UI (Headless) 
options.headless = True
options.add_argument("--headless=new")
  
# initializing webdriver for Chrome with our options 
driver = webdriver.Chrome(options=options) 
  
# getting GeekForGeeks webpage 
driver.get('https://www.geeksforgeeks.org') 
  
# We can also get some information 
# about page in browser. 
# So let's output webpage title into 
# terminal to be sure that the browser 
# is actually running.  
print(driver.title) 
  
# close browser after our manipulations 
driver.close() 