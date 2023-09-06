import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

ticker_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]  

financial_data = {}
for ticker in ticker_symbols:
    stock = yf.Ticker(ticker)
    info = stock.info
    try: financial_data[ticker] = {
        "P/E": info["trailingPE"],
        "P/B": info["priceToBook"],
        "EV/EBITDA": info.get("enterpriseToEbitda", np.nan), 
        "EV/Sales": info.get("enterpriseToRevenue", np.nan)  
        }
    except Exception:
        continue        



df = pd.DataFrame(financial_data)

average_metrics = {
    "P/E": df.loc["P/E"].mean(),
    "P/B": df.loc["P/B"].mean(),
    "EV/EBITDA": df.loc["EV/EBITDA"].mean(),
    "EV/Sales": df.loc["EV/Sales"].mean()
}



ticker_symbol = "AAPL"


apple = yf.Ticker(ticker_symbol)


financial_data = apple.info


market_value = financial_data.get("marketCap", "N/A")
num_shares = financial_data.get("sharesOutstanding", "N/A")
stock_price = financial_data.get("last_price", "N/A")
ebitda = financial_data.get("ebitda", "N/A")
revenues = financial_data.get("revenuePerShare", "N/A")
book_value = int(market_value/financial_data.get("priceToBook", "N/A"))
earnings_per_share = financial_data.get("trailingEps", "N/A")


new_pris_pe = average_metrics['P/E'] * earnings_per_share
new_pris_pb = (average_metrics['P/B'] * book_value) / num_shares
new_pris_ebitda = (average_metrics['EV/EBITDA'] * ebitda) / num_shares
new_pris_revenues = average_metrics['EV/Sales'] * revenues

gjennomsnittlig_pris = (new_pris_pe + new_pris_pb + new_pris_ebitda + new_pris_revenues) / 4

