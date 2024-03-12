"""
    Stock Link - http://www.nasdaq.com/screening/

    MARKET TIME MST - 7:30 AM	2:00 PM
    market time: https://query1.finance.yahoo.com/v6/finance/markettime?formatted=true&key=finance&lang=en-US&region=US

    Stock Algorithm
"""

import csv
import StockLookup
from StockLookup.tms import time, time_type, time_direction
import requests
from StockAlgorithm import StockAlgorithm, StockAlgorithmMethods
import Investopedia
import random
from StocksManager import StockManager, csvReader

SA = StockAlgorithm(StockAlgorithmMethods.simple)

#client = ""
client = Investopedia.Account("astromonkey", 'Masonman0123!')
client.change_game_session("Investopedia Trading Game")

# SETTINGS
risk = 100 # 1+ The Higher the more risk | Recommended to set to 1

period = time_type.day # Grabing data
period_amount = 1 # Grabing data

minimum_price_change = 0.05 # To Buy

minimum_earnings = 0.1 # Total Gain - For Selling

minimum_pe = 15 # For buying
maximum_pe = 25 # For buying

maximum_cost = 4500 # For buying

normal = 1.5 # Used to calculate the amount of stocks to buy, the higher = the more stocks purchased

SA.set_maximum_price(maximum_cost)
SA.set_minimum_earnings(minimum_earnings)
SA.set_minimum_price_change(minimum_price_change)
SA.set_pe(minimum_pe, maximum_pe)
SA.set_normal(normal)
SA.set_risk(risk)

stock_manager = StockManager(client, SA, period_amount, period, csvReader.retrieve_csv_row("stocks.csv", "Symbol"))
stock_manager.start()

#symbol = "DELL"
#SA.set_price_points(StockLookup.get_stock_price_points(symbol, time.time(period_amount, period, time_direction.before), time.now()))
#stock_info = StockLookup.stock_lookup(symbol, time.time(7, period, time_direction.before))#StockLookup.Stock(symbol)#StockLookup.get_stock(symbol)
#print(stock_info.basic.market_price)
#SA.set_pe_ratio(stock_info.trailing_pe_ratio)
#SA.set_stock_price(stock_info.basic.market_price)
#
#print(SA.should_buy())

#stock_info = StockLookup.stock_lookup(symbol, time.time(7, period, time_direction.before))#StockLookup.Stock(symbol)#StockLookup.get_stock(symbol)
#print(stock_info.trailing_pe_ratio)