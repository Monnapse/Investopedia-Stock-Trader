import Investopedia

client = Investopedia.Account("astromonkey", 'Masonman0123!')

#print(client.get_account_overview())
print(client.trade("dell", Investopedia.Action.buy, 1, Investopedia.OrderType.market))
#print(client)