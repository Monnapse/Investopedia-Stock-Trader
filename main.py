"""
    Stock Links
    NYSE - http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nyse&render=download
    NASDAQ - http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=nasdaq&render=download
    AMEX - http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=amex&render=download
"""
import requests

#import Investopedia

#client = Investopedia.Account("astromonkey", 'Masonman0123!')

#print(client.change_game_session("Investopedia Trading Game"))
#print(client.get_account_overview())
#print(client.trade("dell", Investopedia.Action.buy, 5))
print(requests.get("http://www.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true").text)