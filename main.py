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
import os

SA = StockAlgorithm(StockAlgorithmMethods.simple)

client = Investopedia.Account(os.environ["InvestopediaUsername"], os.environ["InvestopediaPassword"])
#client.change_game_session("") # Change this to your game session

#client.sell_all_owned() # You can sell all your stocks with this function

# SETTINGS
risk = 2.5 # 1+ The Higher the more risk | Recommended to set to 1
min_sum = 3 # Min amount of checks for algorithm

period = time_type.day # Grabing data
period_amount = 3 # Grabing data

minimum_price_change = 0.2 # To Buy

minimum_earnings = 0.05 # Total Gain - For Selling

minimum_pe = 15 # For buying
maximum_pe = 25 # For buying

maximum_cost = 1500 # For buying

normal = 1.5 # Used to calculate the amount of stocks to buy, the higher = the more stocks purchased

minimum_account_cash = 15000

sell_check_iterations = 10 # After X stock checks, check if sell needed

SA.set_maximum_price(maximum_cost)
SA.set_minimum_earnings(minimum_earnings)
SA.set_minimum_price_change(minimum_price_change)
SA.set_pe(minimum_pe, maximum_pe)
SA.set_normal(normal)
SA.set_risk(risk)
SA.set_min_sum(min_sum)

stock_manager = StockManager(client, SA, period_amount, period, minimum_account_cash, sell_check_iterations, csvReader.retrieve_csv_row("stocks.csv", "Symbol"))
stock_manager.start()