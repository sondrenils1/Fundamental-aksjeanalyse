import yfinance as yf
import web_finans as fs
import dfc_aker as dfc


tick = "AAPL"
key = "Din API-key. Gå til FinancialModelingPrep.com"
apple = yf.Ticker("AAPL")

utbytte_data = apple.dividends


Key_metrics = fs.get_key_metrics(ticker = tick, limit = 5, key = key)

roe = Key_metrics.loc["roe"][0:5].mean()

dividende_yield = Key_metrics.loc["dividendYield"][0:5].mean()

latest_price = apple.history(period="1d")["Close"].iloc[0]

dividende_per_share = latest_price * dividende_yield

coe = dfc.cost_of_equity()


vekstrate = dividende_yield * roe

dividende_resultat = dividende_per_share / (coe-vekstrate)

     
