from InvestopediaApi import ita

client = ita.Account("astromonkey", 'Masonman0123!')
status = client.get_portfolio_status()
print(status.account_val)