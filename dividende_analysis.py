import yfinance as yf
import web_finans as fs
import dfc_aker as dfc
# Hent data for Apple fra Yahoo Finance

tick = "AAPL"
key = "ecd6d371f7dd586779188ceb26f27a72"
apple = yf.Ticker("AAPL")

# Hent utbyttehistorikk
utbytte_data = apple.dividends

# Anta plowback-ratio og ROE
Key_metrics = fs.get_key_metrics(ticker = tick, limit = 5, key = key)

roe = Key_metrics.loc["roe"][0:5].mean()

dividende_yield = Key_metrics.loc["dividendYield"][0:5].mean()

latest_price = apple.history(period="1d")["Close"].iloc[0]

dividende_per_share = latest_price * dividende_yield

coe = dfc.cost_of_equity()


vekstrate = dividende_yield * roe

dividende_resultat = dividende_per_share / (coe-vekstrate)

"""print(vekstrate)
print(coe)
print(dividende_per_share)
print(dividende_yield)
print(roe)"""

#print(dividende_resultat)
     
