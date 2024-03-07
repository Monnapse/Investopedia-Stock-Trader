"""
    StockLookup
    Made by Monnapse
    Lookup stock info using yahoo finance
"""

import requests
import time
import ProxyApiManager as PAM

wait_time = 20

lookup_sub = "stock_lookup"

yahoo_proxy = PAM.NewProxyApi("yahoo")
yahoo_proxy.add_base_urls([
    "https://query1.finance.yahoo.com", "https://query2.finance.yahoo.com"
])
yahoo_proxy.add_sub(lookup_sub)
yahoo_proxy.add_sub_url(lookup_sub, "/v8/finance/chart/{symbol}?period1={timestamp}&period2={timestamp}")

def get_stock(symbol):
    """
        Gets just the basic info about the stock
    """

    # request
    timestamp = int(time.time())
    #print(yahoo_proxy.get_full_url(lookup_sub).format(symbol=symbol, timestamp=timestamp))
    url = yahoo_proxy.get_full_url(lookup_sub).format(symbol=symbol, timestamp=timestamp)
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
    return {
        "market_price":  data["regularMarketPrice"],
        "currency": data["currency"],
        "exchange_name": data["exchangeName"],
    }