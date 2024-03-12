"""
    Manages your stock trading
"""

import StockLookup
from StockLookup.tms import time, time_type, time_direction
from Investopedia import Action
import time as thread
from datetime import time as time2
import random
from StocksManager import timeChecker

class StockManager():
    def __init__(self, client, stock_algorithm, period_amount, period, minimum_account_cash, sell_check_iterations, tickers) -> None:
        self.client = client
        self.stock_algorithm = stock_algorithm
        self.tickers = tickers
        self.period_amount = period_amount
        self.period = period
        self.minimum_account_balance = minimum_account_cash
        self.account_balance = 0
        self.sell_check_iterations = sell_check_iterations or 5

    def set_tickers(self, tickers):
        self.tickers = tickers
        
    def own_stock(self, symbol):
        if not self.stocks_owned: return False
        for stock in self.stocks_owned:
            if stock.symbol == symbol: return True
        return False
    
    def get_owned_stock(self, symbol):
        if not self.stocks_owned: return
        for stock in self.stocks_owned:
            if stock.symbol == symbol: return stock

    def iterate_stocks(self):
        if not self.tickers: return False # If no tickers to iterate through then return False because execution failed.

        print("Iterating")
        random.shuffle(self.tickers)

        sell_iterations = 0
        iteration = 10
        reset_at = 2

        self.stocks_owned = self.client.get_stocks()

        for ticker in self.tickers:
            if not self.is_market_open(): 
                print("Market is closed")
                break
            #ticker = "AAPL"
            iteration += 1
            sell_iterations += 1

            if iteration >= reset_at:
                # Reset stocks owned
                # Done every 5 stocks searched to stop rate limited
                self.stocks_owned = self.client.get_stocks()
                self.account_balance = float(self.client.get_account_overview()["cash"].replace("$", "").replace(",", ""))
                print("Account balance is", self.account_balance)
                
                iteration = 0

                if sell_iterations >= self.sell_check_iterations: # If iterations have gone through self.sell_check_iterations then check if sell needed
                    sell_iterations = 0
                    print("Checking all owned stocks")
                    for sell_ticker_info in self.stocks_owned:
                        self.stock_algorithm.set_earnings(float(sell_ticker_info.total_change_percent))
                        should_sell = self.stock_algorithm.should_sell()
                        print(should_sell)
                        if should_sell:
                            print("Selling",sell_ticker_info.symbol)
                            self.client.trade(sell_ticker_info.symbol, Action.sell, sell_ticker_info.quantity or 1)
                            thread.sleep(1)

            stock_owned = self.own_stock(ticker)

            self.stock_algorithm.clear_stock_input()

            print(ticker,"Owned",stock_owned)
            
            if stock_owned:
                stock_info = self.get_owned_stock(ticker)
                #print(float(stock_info.total_change_percent))
                self.stock_algorithm.set_earnings(float(stock_info.total_change_percent))
                should_sell = self.stock_algorithm.should_sell()
                print(should_sell)
                if should_sell:
                    print("Selling",ticker)
                    self.client.trade(ticker, Action.sell, stock_info.quantity or 1)
            elif self.account_balance > self.minimum_account_balance:
                price_points = StockLookup.get_stock_price_points(ticker, time.time(self.period_amount, self.period, time_direction.before), time.now())
                #print("Price points", price_points)
                if price_points:
                    self.stock_algorithm.set_price_points(price_points)
                stock_info = StockLookup.stock_lookup(ticker, time.time(1, time_type.year, time_direction.before))

                if stock_info:
                    self.stock_algorithm.set_pe_ratio(stock_info.trailing_pe_ratio)
                    if stock_info.basic:
                        self.stock_algorithm.set_stock_price(stock_info.basic.market_price)

                should_buy, amount = self.stock_algorithm.should_buy()
                #print(should_buy)
                if should_buy:
                    print("Buying", amount, "of", ticker)
                    self.client.trade(ticker, Action.buy, amount or 1)

            thread.sleep(0.1)

    def start(self):
        while True:
            if self.is_market_open():
                print("The Market has opened")
                self.iterate_stocks()
            else:
                print("Market is closed")
            thread.sleep(1)
        
        #print(self.tickers)
            
    def is_market_open(self):
        return timeChecker.is_time_between(time2(7,30), time2(14,00))
        #return timeChecker.is_time_between(time2(7,30), time2(18,00))