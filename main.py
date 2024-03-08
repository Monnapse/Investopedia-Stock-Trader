"""
    Stock Link - http://www.nasdaq.com/screening/

    MARKET TIME MST - 7:30 AM	2:00 PM
    market time: https://query1.finance.yahoo.com/v6/finance/markettime?formatted=true&key=finance&lang=en-US&region=US

    Stock Algorithm
"""

import csv
import StockLookup
from StockLookup.tms import time, time_type, time_direction
import time as thread
import requests

#from requests_oauth2client import BearerAuth

#print(requests.get("https://query1.finance.yahoo.com/v10/finance/quoteSummary/DELL?formatted=true&amp;modules=earnings").content)

#payload = {
#    "code": "a83361f6-cabd-44e8-85a8-be188ca24be9.4bf7bf08-9f08-4746-aeef-44fd00350966.12bddc88-7575-48ef-99f9-f196203e4054",
#    "grant_type": "authorization_code"
#}
#headers = {"Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ0aWpuNDhtZTA1cmJJQ1A0bG9leGVJdTV3dEZ5bG1aVm5VaVpObGxJUU9nIn0.eyJleHAiOjE3MDk4Njg5MjAsImlhdCI6MTcwOTg2ODYyMCwiYXV0aF90aW1lIjoxNzA5ODY4NjE3LCJqdGkiOiI2YWQxYTUzNy01NWY5LTRlZDYtOWM2MC01NjQ5MWQwMjBkN2EiLCJpc3MiOiJodHRwczovL3d3dy5pbnZlc3RvcGVkaWEuY29tL2F1dGgvcmVhbG1zL2ludmVzdG9wZWRpYSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJlM2NmY2UzZC00Y2FmLTRlN2EtYmZiYy0xODgwZDRmYTEwNDQiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJmaW5hbmNlLXNpbXVsYXRvciIsIm5vbmNlIjoiMmM3ODVlMDctNmZhMC00ZjViLTgwYmMtYmE5MDViMzc2Y2Q2Iiwic2Vzc2lvbl9zdGF0ZSI6IjRiZjdiZjA4LTlmMDgtNDc0Ni1hZWVmLTQ0ZmQwMDM1MDk2NiIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL3d3dy5pbnZlc3RvcGVkaWEuY29tL3NpbXVsYXRvciJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtaW52ZXN0b3BlZGlhIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInNpZCI6IjRiZjdiZjA4LTlmMDgtNDc0Ni1hZWVmLTQ0ZmQwMDM1MDk2NiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhc3Ryb21vbmtleSIsImVtYWlsIjoiYXN0cm90cmlnZXJAZ21haWwuY29tIn0.i4YvjEs6kGaVZC3WeShJ7Rmd18DwD47YpBnZb-HVi9iXlLbqxVNISDe76xlhWhZ7Eti7L6aiCX_4kH5O-p45Hu1vAa1IYeGHhJy8l_9Y4iEyos_P91VJ0q2XUbkBdHKlwtndPv2RWqLktSXwNrFiCfud3Bcam9c6f8wDry9rDTTeAiFQXbT02QxQ8OOaJxv7wqO2-BIdBq4VRaW4bFISf5EaG9metg0UV2_GEzu2Xq4314ViD84Pl2KlKysCyagr9CnyXg2OlUsnC6o14qdLlMJf94nnHWQvKIiYCdHIvnWdoxMx9vqdVFRtYdhbr4IyH7JlxWP9tlX42FhpsadcUw"}
#response = requests.post("https://api.investopedia.com/simulator/graphql", headers=headers, auth = HTTPBasicAuth('astromonkey', 'Masonman0123'))
#token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJ0aWpuNDhtZTA1cmJJQ1A0bG9leGVJdTV3dEZ5bG1aVm5VaVpObGxJUU9nIn0.eyJleHAiOjE3MDk4Njg5MjAsImlhdCI6MTcwOTg2ODYyMCwiYXV0aF90aW1lIjoxNzA5ODY4NjE3LCJqdGkiOiI2YWQxYTUzNy01NWY5LTRlZDYtOWM2MC01NjQ5MWQwMjBkN2EiLCJpc3MiOiJodHRwczovL3d3dy5pbnZlc3RvcGVkaWEuY29tL2F1dGgvcmVhbG1zL2ludmVzdG9wZWRpYSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJlM2NmY2UzZC00Y2FmLTRlN2EtYmZiYy0xODgwZDRmYTEwNDQiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJmaW5hbmNlLXNpbXVsYXRvciIsIm5vbmNlIjoiMmM3ODVlMDctNmZhMC00ZjViLTgwYmMtYmE5MDViMzc2Y2Q2Iiwic2Vzc2lvbl9zdGF0ZSI6IjRiZjdiZjA4LTlmMDgtNDc0Ni1hZWVmLTQ0ZmQwMDM1MDk2NiIsImFsbG93ZWQtb3JpZ2lucyI6WyJodHRwczovL3d3dy5pbnZlc3RvcGVkaWEuY29tL3NpbXVsYXRvciJdLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImRlZmF1bHQtcm9sZXMtaW52ZXN0b3BlZGlhIl19LCJyZXNvdXJjZV9hY2Nlc3MiOnsiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInNpZCI6IjRiZjdiZjA4LTlmMDgtNDc0Ni1hZWVmLTQ0ZmQwMDM1MDk2NiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhc3Ryb21vbmtleSIsImVtYWlsIjoiYXN0cm90cmlnZXJAZ21haWwuY29tIn0.i4YvjEs6kGaVZC3WeShJ7Rmd18DwD47YpBnZb-HVi9iXlLbqxVNISDe76xlhWhZ7Eti7L6aiCX_4kH5O-p45Hu1vAa1IYeGHhJy8l_9Y4iEyos_P91VJ0q2XUbkBdHKlwtndPv2RWqLktSXwNrFiCfud3Bcam9c6f8wDry9rDTTeAiFQXbT02QxQ8OOaJxv7wqO2-BIdBq4VRaW4bFISf5EaG9metg0UV2_GEzu2Xq4314ViD84Pl2KlKysCyagr9CnyXg2OlUsnC6o14qdLlMJf94nnHWQvKIiYCdHIvnWdoxMx9vqdVFRtYdhbr4IyH7JlxWP9tlX42FhpsadcUw"
#headers = {
#  "Cookie": "AUTH_SESSION_ID=4bf7bf08-9f08-4746-aeef-44fd00350966; AUTH_SESSION_ID_LEGACY=4bf7bf08-9f08-4746-aeef-44fd00350966; KEYCLOAK_SESSION_LEGACY=investopedia/e3cfce3d-4caf-4e7a-bfbc-1880d4fa1044/4bf7bf08-9f08-4746-aeef-44fd00350966; KEYCLOAK_SESSION=investopedia/e3cfce3d-4caf-4e7a-bfbc-1880d4fa1044/4bf7bf08-9f08-4746-aeef-44fd00350966; KEYCLOAK_IDENTITY_LEGACY=eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI0YWM2ZjA4Yy0wNWFmLTQzNTctYmExOS01MzYxNzE2ZDg0YjkifQ.eyJleHAiOjE3MTI0NjIwNjIsImlhdCI6MTcwOTg3MDA2MiwianRpIjoiZDQzZjhhNzAtOTk3OC00NDYxLWE4NDctYjI5YTg5N2RhNzQyIiwiaXNzIjoiaHR0cHM6Ly93d3cuaW52ZXN0b3BlZGlhLmNvbS9hdXRoL3JlYWxtcy9pbnZlc3RvcGVkaWEiLCJzdWIiOiJlM2NmY2UzZC00Y2FmLTRlN2EtYmZiYy0xODgwZDRmYTEwNDQiLCJ0eXAiOiJTZXJpYWxpemVkLUlEIiwic2Vzc2lvbl9zdGF0ZSI6IjRiZjdiZjA4LTlmMDgtNDc0Ni1hZWVmLTQ0ZmQwMDM1MDk2NiIsInNpZCI6IjRiZjdiZjA4LTlmMDgtNDc0Ni1hZWVmLTQ0ZmQwMDM1MDk2NiIsInN0YXRlX2NoZWNrZXIiOiJucnBQbFFTcjMtOHlnbkFLUTNfbm15QVVaOURXb1ROdzlYdGRfSzdFN1RFIn0.Tz8-3_Be4hF6sKEC2GkHAwE7-rj6IWR3dVCVlVEl8xE; KEYCLOAK_IDENTITY=eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI0YWM2ZjA4Yy0wNWFmLTQzNTctYmExOS01MzYxNzE2ZDg0YjkifQ.eyJleHAiOjE3MTI0NjIwNjIsImlhdCI6MTcwOTg3MDA2MiwianRpIjoiZDQzZjhhNzAtOTk3OC00NDYxLWE4NDctYjI5YTg5N2RhNzQyIiwiaXNzIjoiaHR0cHM6Ly93d3cuaW52ZXN0b3BlZGlhLmNvbS9hdXRoL3JlYWxtcy9pbnZlc3RvcGVkaWEiLCJzdWIiOiJlM2NmY2UzZC00Y2FmLTRlN2EtYmZiYy0xODgwZDRmYTEwNDQiLCJ0eXAiOiJTZXJpYWxpemVkLUlEIiwic2Vzc2lvbl9zdGF0ZSI6IjRiZjdiZjA4LTlmMDgtNDc0Ni1hZWVmLTQ0ZmQwMDM1MDk2NiIsInNpZCI6IjRiZjdiZjA4LTlmMDgtNDc0Ni1hZWVmLTQ0ZmQwMDM1MDk2NiIsInN0YXRlX2NoZWNrZXIiOiJucnBQbFFTcjMtOHlnbkFLUTNfbm15QVVaOURXb1ROdzlYdGRfSzdFN1RFIn0.Tz8-3_Be4hF6sKEC2GkHAwE7-rj6IWR3dVCVlVEl8xE; TMog=ncec8f7eba4224443a978d7b6e623300403; globalTI_SID=c66de77f-fcd5-40da-822e-207a1e52fdb0; lb_ld=search; _gcl_au=1.1.1619976232.1709731981; _ga=GA1.2.1155517574.1709731987; __gads=ID=3829989c813d685e:T=1709731988:RT=1709731988:S=ALNI_MYYADMD8lvz-OFOkvvUlAAMTXu9dQ; __gpi=UID=00000dc617d10068:T=1709731988:RT=1709731988:S=ALNI_MZX0a4EQlflvdFlC3sGOgzLBQsBdw; __eoi=ID=abe3a1edc874a989:T=1709731988:RT=1709731988:S=AA-Afjah_9F5sIwsSE81RdkQ17HV; _gid=GA1.2.409947621.1709818566; _pbjs_userid_consent_data=3524755945110770; Mint=nec0ab0976a29479581fb8ef6b2b2e17303; pc=1; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Mar+07+2024+20%3A54%3A22+GMT-0700+(Mountain+Standard+Time)&version=202310.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=4d2a93a2-2c15-4b99-b3dd-c686cbbaad96&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2CBG111%3A1%2C4%3A1&AwaitingReconsent=false; AWSALB=wMlCJHnS99gfuQGcI1LlGP6IrUVBjjYidfvFofl9m/yAJ9XqCAZaj1ELUOkWEwJUIbsqO5hXF99488IuA3UcFtB4VAI+HSLrUMsHhZO7/wqlfUvO9IKImmVdgMy3; AWSALBCORS=wMlCJHnS99gfuQGcI1LlGP6IrUVBjjYidfvFofl9m/yAJ9XqCAZaj1ELUOkWEwJUIbsqO5hXF99488IuA3UcFtB4VAI+HSLrUMsHhZO7/wqlfUvO9IKImmVdgMy3"
#}

#response = requests.post("https://api.investopedia.com/simulator/graphql", headers=headers, auth=BearerAuth(token))
#response = requests.post("https://www.investopedia.com/auth/realms/investopedia/protocol/openid-connect/token", headers=headers, data=payload)
#print(response.content)




import Investopedia

client = Investopedia.Account("astromonkey", 'Masonman0123!')
client.change_game_session("Investopedia Trading Game")

for stock in client.get_stocks():
    print(stock.symbol, stock.quantity)

#e = '$1.00\n(0.17%)'
#d,p = e.replace("(","").replace(")","").replace("%","").replace("$","").split("\n")
#print()

#print(1709859599 - datetime.timedelta(weeks = 52.1429).days)

#print(time.time(1, time_type.year, time_direction.away))
#print(time.now())

#print(StockLookup.stock_lookup("DELL", time.time(1, time_type.year, time_direction.before)).quarterly_pe_ratio)
"""
with open('stocks.csv', mode ='r') as file:
  csvFile = csv.DictReader(file)
  for row in csvFile:
        #print(yf.Ticker(row["Symbol"]).fast_info.last_price)
        symbol = row["Symbol"]
        #stock_info = yf.Ticker(row["Symbol"]).fast_info
        #print(stock_info.last_price)
        stock_info = StockLookup.stock_lookup(symbol, time.time(1, time_type.year, time_direction.before))#StockLookup.Stock(symbol)#StockLookup.get_stock(symbol)
        if stock_info:
            print(stock_info.quarterly_pe_ratio)
        #if stock_info and stock_info != None and stock_info.market_price > 1 and stock_info.market_price < 1000:
        #    client.trade(symbol, Investopedia.Action.buy, 1)

        thread.sleep(0.1)
"""