"""
    Stock Link - http://www.nasdaq.com/screening/

    9:30 AM - 4:00 PM
"""
#import requests
#import csv
#import pandas
#import yfinance as yf
#import time
#from bs4 import BeautifulSoup
#import StockLookup
import StockLookup

print(StockLookup.get_stock("DELL"))

#kroger = stockquotes.Stock('KR')
#print(kroger.current_price)

#import Investopedia

#soup = BeautifulSoup(requests.get("https://finance.yahoo.com/quote/DELL").content, "html.parser")
#key = soup.select('/html/body/div[1]/main/section/section/section/article/section[1]/div[2]/div[1]/section/div/section/div[1]/fin-streamer[1]/span')
#print(key)
#client = Investopedia.Account("astromonkey", 'Masonman0123!')

#print(client.change_game_session("Investopedia Trading Game"))
#print(client.get_account_overview())
#print(client.trade("dell", Investopedia.Action.buy, 5))

"""
with open('stocks.csv', mode ='r')as file:
  csvFile = csv.DictReader(file)
  for row in csvFile:
        #print(yf.Ticker(row["Symbol"]).fast_info.last_price)
        symbol = row["Symbol"]
        stock_info = yf.Ticker(row["Symbol"]).fast_info
        print(stock_info.last_price)
        #if stock_info.last_price > 1 and stock_info.last_price < 1000:
        #    client.trade(symbol, Investopedia.Action.buy, 1)
        time.sleep(0.1)
        """
        
#dell = yf.Ticker("DELL")
#print(dell.fast_info.last_price)
#print(StockLookup.get_stock("DELL"))