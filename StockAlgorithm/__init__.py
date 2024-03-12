"""
    STOCK ALGORITHM
    Made by Monnapse
"""

import math

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
    if len(prices) <= 0: return
    initial_price = prices[0]
    percentage_changes = [(price - initial_price) / initial_price * 100 for price in prices]
    percentage_change = 0
    for i in percentage_changes:
        percentage_change+=i
    return percentage_change/len(prices)

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
        #self.stock_change = 0

        self.earnings = None
        self.pe_ratio = None
        self.price_points = []

    def set_price_points(self, price_points: list):
        self.price_points = price_points

    def set_pe_ratio(self, pe_ratio):
        if not pe_ratio: return
        self.pe_ratio = float(pe_ratio)

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

    def get_price_change(self):
        formated_list = []
        for i in self.price_points:
            formated_list.append(i[0])
        return calculate_total_price_change(formated_list)

    def should_buy(self):
        #avg_angle = math.pi/2 - average_angle(self.price_points)
        #print('Average Angle:', math.degrees(avg_angle))
        price_change_buy = False
        price_change = self.get_price_change() or 0
        #print(self.minimum_price_change, price_change)
        if self.minimum_price_change and float(price_change) < float(self.minimum_price_change):
            price_change_buy = True

        pe_ratio_buy = False
        pe_ratio = self.pe_ratio
        #print("PE RATIO", pe_ratio)
        max_pe = (self.maximum_pe or 99999999999) * self.risk
        #print(max_pe)
        if not pe_ratio: pe_ratio_buy = True
        elif pe_ratio and pe_ratio > self.minimum_pe and pe_ratio < max_pe:
            pe_ratio_buy = True
            #print("GOOD")

        #print(price_change_buy, pe_ratio_buy)
            
        self.price_points = []
        self.pe_ratio = None

        return pe_ratio_buy and price_change_buy
    
    def should_sell(self):
        if not self.earnings: return False
        if self.earnings > self.minimum_earnings: True