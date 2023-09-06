import yfinance as yf
import numpy as np
import pandas as pd
import web_finans as fs
import requests


tick = "AAPL"
stock_data = yf.Ticker(tick)



key = "Din API-key. Gå til FinancialModelingPrep.com"

IM = fs.get_industry_multiples()

full_financial_statement = fs.get_full_financial_statement_as_reported(ticker = tick, key = key, period = 'quarter')


IS = fs.get_income_statement(ticker = tick, limit = 5, key = key, period = 'quarter')

BS = fs.get_balance_sheet(ticker = tick, limit = 5, key = key, period = 'quarter')

CF = fs.get_cash_flow_statement(ticker = tick, limit = 5, key = key, period = 'quarter')



inflation_target = 0.02

def cost_of_equity():
    
    """yield_us = yf.Ticker("^TNX")
    yield_now = yield_us.history(period="1d")["Close"].iloc[0]

    stock_data_capm = yf.Ticker(ticker_symbol).history(period="5y")"""




    
    stock_beta = stock_data.info["beta"]
    
    market_risk_premium = 0.057  # 5.7%

   
    coe = inflation_target + (stock_beta * (market_risk_premium))

    return coe

def cost_of_debt(): 

    
    default_spread = 0.035
    tax_rate = 0.21
    rating_risk = default_spread + inflation_target
    COD = rating_risk*(1-tax_rate)
    return COD



def WACC():
    equity = BS.loc["totalEquity"][0]
    debt = BS.loc['totalDebt'][0]
    equity_weight = fs.get_market_capital(tick,key) / (fs.get_market_capital(tick,key) + BS.loc['totalDebt'][0])
    debt_weight = BS.loc['totalDebt'][0] / (fs.get_market_capital(tick,key) + BS.loc['totalDebt'][0])
  
    WACC = equity_weight*cost_of_equity() + debt_weight*cost_of_debt()
  
    return WACC

def excpect_growth_rate():
    
    #Setter den litt over inflasjonen
    return 0.03


def excpected_free_cash_flow():
    ATOIs = []
    for i in range(0, 5):
       
        ATOIs.append(CF.loc["freeCashFlow"][i])
    years = 5
   

    ATOI_growth = []
    discount_rate = WACC()
    ATOI_discount = []
    vekstrate = []

    for i in range(0, years-1):
        vekstrate.append(ATOIs[i]/ATOIs[i+1])

    snitt_vekstrate = sum(vekstrate)/len(vekstrate)
    ny_snitt_vekstrate = (snitt_vekstrate + excpect_growth_rate()) / 2

    #Antagelse om at Apple øker med ca 10% i CAGR hvert år. Går an å sette opp budsjettert, og komme seg fram sånn ca
    #Men per nå er det antagelse om ca 10% i vekst i cashflow. Det stemmer helt ok historisk sett også
    
    for i in range(0, years):
        ATOI_growth.append(ATOIs[0]*(1.1)**(i+1))
        ATOI_discount.append(ATOI_growth[i]/((1+discount_rate)**(i+1)))
   


    return ATOI_discount, ATOI_growth



    


def calculate_terminal_value():
    
    ATOI= excpected_free_cash_flow()[1]
    siste_FFCF = ATOI[4]
    Terminal_Value = (siste_FFCF*(1+excpect_growth_rate()))/(WACC()-excpect_growth_rate())
    return Terminal_Value




pv_terminal_value = calculate_terminal_value() / ((1 + WACC())**5)
enterprise_value = pv_terminal_value + sum(excpected_free_cash_flow()[0])

equity_value = enterprise_value - BS.loc['totalDebt'][0]

num_shares = fs.get_quote(tick, key).loc['sharesOutstanding'][0]
rating = equity_value / num_shares


