"""
    Stock Link - http://www.nasdaq.com/screening/

    MARKET TIME MST - 7:30 AM	2:00 PM
    market time: https://query1.finance.yahoo.com/v6/finance/markettime?formatted=true&key=finance&lang=en-US&region=US

    Stock Algorithm
"""

import csv
import StockLookup
from StockLookup.tms import time, time_type, time_direction
import time as thread
import requests
from StockAlgorithm import StockAlgorithm, StockAlgorithmMethods
import Investopedia

SA = StockAlgorithm(StockAlgorithmMethods.simple)

client = Investopedia.Account("astromonkey", 'Masonman0123!')
client.change_game_session("Investopedia Trading Game")

# SETTINGS
risk = 100 # 1+ The Higher the more risk | Recommended to set to 1

period = time_type.day
period_amount = 1

minimum_price_change = 0.01

minimum_earnings = 10 # Total Gain

minimum_pe = 15
maximum_pe = 25

SA.set_minimum_earnings(minimum_earnings)
SA.set_minimum_price_change(minimum_price_change)
SA.set_pe(minimum_pe, maximum_pe)
SA.set_risk(risk)

#symbol = "DELL"
#SA.set_price_points(StockLookup.get_stock_price_points(symbol, time.time(period_amount, period, time_direction.before), time.now()))
#stock_info = StockLookup.stock_lookup(symbol, time.time(7, period, time_direction.before))#StockLookup.Stock(symbol)#StockLookup.get_stock(symbol)
#print(stock_info.trailing_pe_ratio)
#SA.set_pe_ratio(stock_info.trailing_pe_ratio)
#print(SA.should_buy())

#stock_info = StockLookup.stock_lookup(symbol, time.time(7, period, time_direction.before))#StockLookup.Stock(symbol)#StockLookup.get_stock(symbol)
#print(stock_info.trailing_pe_ratio)

with open('stocks.csv', mode ='r') as file:
  csvFile = csv.DictReader(file)
  for row in csvFile:
        #print(yf.Ticker(row["Symbol"]).fast_info.last_price)
        symbol = row["Symbol"]
        #stock_info = yf.Ticker(row["Symbol"]).fast_info/
        #print(stock_info.last_price)
        price_points = StockLookup.get_stock_price_points(symbol, time.time(period_amount, period, time_direction.before), time.now())
        if price_points:
            SA.set_price_points(price_points)

        stock_info = StockLookup.stock_lookup(symbol, time.time(1, time_type.year, time_direction.before))#StockLookup.Stock(symbol)#StockLookup.get_stock(symbol)
        if stock_info:
            SA.set_pe_ratio(stock_info.trailing_pe_ratio)
        #if stock_info and stock_info != None and stock_info.market_price > 1 and stock_info.market_price < 1000:
        #    client.trade(symbol, Investopedia.Action.buy, 1)
            
        if SA.should_buy():
            client.trade(symbol, Investopedia.Action.buy, 1)

        thread.sleep(0.1)