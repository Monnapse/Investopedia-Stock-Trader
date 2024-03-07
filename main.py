"""
    Stock Link - http://www.nasdaq.com/screening/
"""
import requests
import csv
import pandas
import yfinance as yf
import time

import Investopedia

client = Investopedia.Account("astromonkey", 'Masonman0123!')

print(client.change_game_session("Investopedia Trading Game"))
#print(client.get_account_overview())
#print(client.trade("dell", Investopedia.Action.buy, 5))

with open('stocks.csv', mode ='r')as file:
  csvFile = csv.DictReader(file)
  for row in csvFile:
        #print(yf.Ticker(row["Symbol"]).fast_info.last_price)
        symbol = row["Symbol"]
        stock_info = yf.Ticker(row["Symbol"]).fast_info
        if stock_info.last_price > 1 and stock_info.last_price < 1000:
            client.trade(symbol, Investopedia.Action.buy, 1)
        time.sleep(0.1)
        
#dell = yf.Ticker("DELL")
#print(dell.fast_info.last_price)