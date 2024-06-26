"""
    STOCK ALGORITHM
    Made by Monnapse
"""

import math
import re

def calculate_angle(x1, y1, x2, y2):
    # Calculate the angle between two points relative to the horizontal axis
    return math.atan2(y2 - y1, x2 - x1)

def average_angle(points):
    # Calculate the total sum of sine and cosine components of all angles
    sin_sum = 0
    cos_sum = 0
    
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        angle = calculate_angle(x1, y1, x2, y2)
        sin_sum += math.sin(angle)
        cos_sum += math.cos(angle)
    
    # Calculate the average angle from the sum of sine and cosine components
    avg_angle = math.atan2(sin_sum / len(points), cos_sum / len(points))
    
    return avg_angle

def calculate_total_price_change(prices):
    total_change = sum(prices[i] - prices[i - 1] for i in range(1, len(prices)))
    return total_change

class StockAlgorithmMethods:
    simple = "simple"

class StockAlgorithm:
    def __init__(self, method) -> None:
        self.method = method
        self.minimum_earnings = 1
        self.minimum_price_change = 0
        self.minimum_pe = 15
        self.maximum_pe = None
        self.risk = 1
        self.normal = 1
        self.maximum_price = None
        self.min_sum = 2
        #self.stock_change = 0

        self.stock_price = None
        self.earnings = None
        self.pe_ratio = None
        self.analyst = None
        self.price_points = []

    def set_min_sum(self, min_sum):
        self.min_sum = min_sum

    def set_price_points(self, price_points: list):
        self.price_points = price_points

    def set_normal(self, normal):
        self.normal = normal

    def set_pe_ratio(self, pe_ratio):
        if not pe_ratio: return
        self.pe_ratio = float(re.sub(r'[^0-9.]', '', pe_ratio))

    def set_change(self, change: float):
        self.price_points = change

    def set_minimum_price_change(self, price_change):
        self.minimum_price_change = price_change

    def set_pe(self, minimum, maximum):
        self.minimum_pe = minimum
        self.maximum_pe = maximum
    
    def set_risk(self, risk):
        self.risk = risk

    def set_minimum_earnings(self, minimum):
        self.minimum_earnings = minimum
    
    def set_earnings(self, earnings):
        self.earnings = earnings

    def set_stock_price(self, price):
        self.stock_price = price
        #print(self.stock_price)

    def set_analyst(self, analyst):
        self.analyst = analyst

    def set_maximum_price(self, maximum):
        self.maximum_price = maximum

    def get_price_change(self):
        formated_list = []
        for i in self.price_points:
            formated_list.append(i[0])
        return calculate_total_price_change(formated_list)

    def should_buy(self, symbol:str = ""):
        #avg_angle = math.pi/2 - average_angle(self.price_points)
        #print('Average Angle:', math.degrees(avg_angle))
        sum = 0

        price_change = self.get_price_change() or 0
        #print(self.minimum_price_change, price_change)
        if self.minimum_price_change and float(price_change) > float(self.minimum_price_change):
            sum += 1

        #pe_ratio_buy = False
        pe_ratio = self.pe_ratio or 1
        #print("PE RATIO", pe_ratio)
        max_pe = (self.maximum_pe or 99999999999) * self.risk
        #print(max_pe)
        if pe_ratio and pe_ratio > self.minimum_pe and pe_ratio < max_pe:
            sum += 1
            #pe_ratio_buy = True
            #print("GOOD")

        #print(price_change_buy, pe_ratio_buy)
        
        if self.analyst and self.analyst == "Buy" or self.analyst == "Strong Buy":
            sum += 1

        buy = sum >= self.min_sum
        amount = 0

        if buy:
            stock_price = self.stock_price or 10
            normal = self.normal or 1

            #print(self.stock_price)
            #print(normal,stock_price,price_change,pe_ratio)
            amount = abs(round((normal/stock_price)*abs(100/price_change)*abs(pe_ratio) or 15))
            if amount*stock_price > self.maximum_price:
               amount = abs(round(self.maximum_price/stock_price))
            print(f"Symbol: {symbol}, Stock Price: ${str(stock_price)}, Price Change {str(price_change)}%, PE Ratio: {str(pe_ratio)}, Stock Amount: {str(amount)}, Price: {str(amount*stock_price)}")
            #print("Would cost you:", amount*stock_price)
            #amount = 1
        else:
            print(f"Symbol: {symbol}, Sum: {sum}")


        self.clear_stock_input()
        return buy, amount
    
    def should_sell(self):
        #print (self.earnings)
        if not self.earnings: return False
        if self.earnings > self.minimum_earnings: return True

        self.clear_stock_input()

    def clear_stock_input(self):
        self.stock_price = None
        self.earnings = None
        self.pe_ratio = None
        self.price_points = []