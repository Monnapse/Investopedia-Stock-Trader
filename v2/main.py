import Investopedia

client = Investopedia.Account("astromonkey", 'Masonman0123!')
client.set_headless()

print(client.get_account_overview())

#print(client)