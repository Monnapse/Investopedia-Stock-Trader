"""
    Stock Link - http://www.nasdaq.com/screening/
"""
import requests
import csv
import pandas

#import Investopedia

#client = Investopedia.Account("astromonkey", 'Masonman0123!')

#print(client.change_game_session("Investopedia Trading Game"))
#print(client.get_account_overview())
#print(client.trade("dell", Investopedia.Action.buy, 5))

#with open('stocks.csv', mode ='r')as file:
#  csvFile = csv.DictReader(file)
#  for row in csvFile:
#        print(row["Symbol"])
#        
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
r = requests.get(url)
data = r.json()

print(data)