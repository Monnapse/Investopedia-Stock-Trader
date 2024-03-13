"""
    StockLookup
    Made by Monnapse
    Lookup stock info using yahoo finance, nasdaq

    get crumb: https://query1.finance.yahoo.com/v1/test/getcrumb
    nasdaq analyst rating: https://api.nasdaq.com/api/analyst/DELL/ratings
"""

import requests
import time
import ProxyApiManager as PAM
import datetime
from enum import Enum

wait_time = 20

basic_lookup_sub = "basic_lookup_sub"
advanced_lookup_sub = "advanced_lookup_sub"
analyst_rating = "analyst_rating"

yahoo_api = PAM.NewProxyApi("yahoo")
yahoo_api.add_base_urls([
    "https://query1.finance.yahoo.com", "https://query2.finance.yahoo.com"
])
yahoo_api.add_sub(basic_lookup_sub)
yahoo_api.add_sub_url(basic_lookup_sub, "/v8/finance/chart/{symbol}?period1={period1}&period2={period2}")
yahoo_api.add_sub_url(basic_lookup_sub, "/v7/finance/chart/{symbol}?period1={period1}&period2={period2}")

yahoo_api.add_sub(advanced_lookup_sub)
yahoo_api.add_sub_url(advanced_lookup_sub, "/ws/fundamentals-timeseries/v1/finance/timeseries/{symbol}?merge=false&padTimeSeries=true&period1={period1}&period2={period2}&type=quarterlyMarketCap%2CtrailingMarketCap%2CquarterlyEnterpriseValue%2CtrailingEnterpriseValue%2CquarterlyPeRatio%2CtrailingPeRatio%2CquarterlyForwardPeRatio%2CtrailingForwardPeRatio%2CquarterlyPegRatio%2CtrailingPegRatio%2CquarterlyPsRatio%2CtrailingPsRatio%2CquarterlyPbRatio%2CtrailingPbRatio%2CquarterlyEnterprisesValueRevenueRatio%2CtrailingEnterprisesValueRevenueRatio%2CquarterlyEnterprisesValueEBITDARatio%2CtrailingEnterprisesValueEBITDARatio&lang=en-US&region=US")

nasdaq_api = PAM.NewProxyApi("nasdaq")
nasdaq_api.add_base("https://api.nasdaq.com")
nasdaq_api.add_sub(analyst_rating)
nasdaq_api.add_sub_url(analyst_rating, "/api/analyst/{symbol}/ratings")

class basic_stock_info:
    market_price = int
    currency = str
    exchange_name = str

class stock_info:
    symbol = None
    basic = None
    quarterly_market_cap = None
    trailing_market_cap = None
    quarterly_enterprise_value = None
    trailing_enterprise_value = None
    quarterly_pe_ratio = None
    trailing_pe_ratio = None
    quarterly_forward_pe_ratio = None
    trailing_forward_pe_ratio = None
    quarterly_peg_ratio = None
    trailing_peg_ratio = None
    quarterly_ps_ratio = None
    trailing_ps_ratio = None
    quarterly_pb_ratio = None
    trailing_pb_ratio = None
    quarterly_enterprises_value_revenue_ratio = None
    trailing_enterprises_value_revenue_ratio = None
    quarterly_enterprises_value_ebitda_ratio = None
    trailing_enterprises_value_ebitda_ratio = None
    analyst_rating = None

def basic_stock_lookup(symbol) -> basic_stock_info:
    """
        Gets just the basic info about the stock
    """

    # request
    timestamp = int(time.time())
    #print(yahoo_api.get_full_url(lookup_sub).format(symbol=symbol, timestamp=timestamp))
    url = yahoo_api.get_full_url(basic_lookup_sub).format(symbol=symbol, period1=timestamp, period2=timestamp)
    print(url)
    headers = {
        "User-Agent": "curl/7.68.0"
    }
    response = requests.get(url, headers=headers)
    #print(response.headers)
    #print(response.content)
    response_json = response.json()
    #print(response_json["chart"]["result"][0]["meta"]["regularMarketPrice"])
    if response_json == None or response_json == 'NoneType': return None
    
    result = response_json["chart"]["result"]
    
    if result == None: return

    data = result[0]["meta"]
    #return {
    #    "market_price":  data["regularMarketPrice"],
    #    "currency": data["currency"],
    #    "exchange_name": data["exchangeName"],
    #}

    stock_info = basic_stock_info()
    stock_info.market_price = data["regularMarketPrice"]
    stock_info.currency = data["currency"]
    stock_info.exchange_name = data["exchangeName"]

    return stock_info

def format_camel_case(string: str):
    new_string = ""
    for i in list(string):
        if i.isupper():
            new_string = new_string + "_" + i.lower()
        else:
            new_string = new_string + i
    return new_string

def stock_lookup(symbol, period1: int=None, period2: int=None) -> stock_info:
    """
        More advanced stock lookup
        https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries/DELL?merge=false&padTimeSeries=true&period1=1694127600&period2=1709859599&type=quarterlyMarketCap%2CtrailingMarketCap%2CquarterlyEnterpriseValue%2CtrailingEnterpriseValue%2CquarterlyPeRatio%2CtrailingPeRatio%2CquarterlyForwardPeRatio%2CtrailingForwardPeRatio%2CquarterlyPegRatio%2CtrailingPegRatio%2CquarterlyPsRatio%2CtrailingPsRatio%2CquarterlyPbRatio%2CtrailingPbRatio%2CquarterlyEnterprisesValueRevenueRatio%2CtrailingEnterprisesValueRevenueRatio%2CquarterlyEnterprisesValueEBITDARatio%2CtrailingEnterprisesValueEBITDARatio&lang=en-US&region=US
        
        Parameters:
            period1 (int) : Grabs stock info starting from this time.
            period2 (int) : Grabs stock info ending at this time.
        
        Includes the following info
            * market price
            * currency
            * exchange name
            * quarterly market cap
            * trailing market cap
            * quarterly enterprise value
            * trailing enterprise value
            * quarterly pe ratio
            * trailing pe Ratio
            * quarterly forward pe ratio
            * trailing forward peratio
            * quarterly Pegratio
            * trailing peg ratio
            * quarterly ps ratio
            * trailing ps ratio
            * quarterly pb ratio
            * trailing pb ratio
            * quarterly enterprises value revenue ratio
            * trailing enterprises value revenue ratio
            * quarterly enterprises value EBITDA ratio
            * trailing enterprises value EBITDA ratio
    """
    # Set basic values
    stock = stock_info()
    stock.symbol = symbol
    stock.basic = basic_stock_lookup(symbol)

    # Check if period1 or period2 are none if so then set to current time
    current_timestamp = int(time.time())
    if period1 == None:
        period1 = current_timestamp
    if period2 == None:
        period2 = current_timestamp


    # Yahoo Finance data
    url = yahoo_api.get_full_url(advanced_lookup_sub).format(symbol=symbol, period1=period1, period2=period2)
    headers = {
        "User-Agent": "curl/7.68.0"
    }
    response = requests.get(url, headers=headers)
    response_json = response.json()
    #print(response_json)
    if response_json != None and response_json != 'NoneType':
        results = response_json["timeseries"]["result"]
        for i in results:
            stock_info_meta = i["meta"]
            meta_type: str = i["meta"]["type"][0]

            if i.get(meta_type):
                meta_type_list = i[meta_type]
                meta_value = meta_type_list[len(meta_type_list)-1]
                if meta_value :
                    meta_value = meta_value["reportedValue"]["fmt"]
                    setattr(stock, format_camel_case(meta_type), meta_value)

    # Nasdaq Data
    url = nasdaq_api.get_full_url(analyst_rating).format(symbol=symbol)

    analyst_headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent":"Java-http-client/"
    }
    response = requests.get(url, headers=analyst_headers)

    response_json = response.json()
    if response_json != None and response_json != 'NoneType':
        data = response_json["data"]
        if data:
            stock_info.analyst_rating = data["meanRatingType"]
            
    return stock

def get_stock_price_points(symbol: str, period1: int=None, period2: int=None) -> list:
    url = yahoo_api.get_full_url(basic_lookup_sub).format(symbol=symbol, period1=str(period1), period2=str(period2))
    print(url)
    headers = {
        "User-Agent": "curl/7.68.0"
    }
    response = requests.get(url, headers=headers)
    #print(response.headers)
    #print(response.content)
    response_json = response.json()
    #print(response_json["chart"]["result"][0]["meta"]["regularMarketPrice"])
    if response_json == None or response_json == 'NoneType' or not response_json.get("chart"): return None
    
    result = response_json["chart"]["result"]

    if result == None: return
    data = None
    try:
        data = result[0]["indicators"]["quote"][0].get("open")
    except:
        return
    if not data: return
    #nodes = ""
    price_points = []
    index = 0
    for i in data:
        if i == None: 
            continue
        #if index != 0:
        #    nodes = nodes+","

        index += 1

        #print(format_time(index))
        #nodes = nodes+str(i)+","+str(index)
        price_points.append([i, index])
    return price_points