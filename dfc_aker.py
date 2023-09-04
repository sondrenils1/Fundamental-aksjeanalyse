import yfinance as yf
import numpy as np
import pandas as pd
import web_finans as fs
import requests


tick = "AAPL"
stock_data = yf.Ticker(tick)



key = "ecd6d371f7dd586779188ceb26f27a72"

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



"""def cash_flow():
    FCFF = (sum(IS.loc['netIncome'][0:5]) + sum(IS.loc['interestExpense'][0:5]) + sum(IS.loc['incomeTaxExpense'][0:5]))*(1-0.21) - (sum(CF.loc['capitalExpenditure'][0:5]) - full_financial_statement.loc['depreciationdepletionandamortization'][0:5].sum()) -  sum(CF.loc['changeInWorkingCapital'][0:5])
    return FCFF/1000000000"""

def WACC():
    equity = BS.loc["totalEquity"][0]
    debt = BS.loc['totalDebt'][0]
    equity_weight = fs.get_market_capital(tick,key) / (fs.get_market_capital(tick,key) + BS.loc['totalDebt'][0])
    debt_weight = BS.loc['totalDebt'][0] / (fs.get_market_capital(tick,key) + BS.loc['totalDebt'][0])
    #print(BS.loc['totalDebt'][0])
    #print(BS.loc["totalEquity"][0])
    #print(debt/equity)
    #print(equity_weight, debt_weight)
    WACC = equity_weight*cost_of_equity() + debt_weight*cost_of_debt()
    #print("Dette er WACC" + str(WACC))
    return WACC

def excpect_growth_rate():
    #reinvestment_rate = ((-1)*sum(CF.loc['capitalExpenditure'][0:5]) - sum(IS.loc['depreciationAndAmortization'][0:5]) + sum(CF.loc['changeInWorkingCapital'][0:5])) / (sum(IS.loc['netIncome'][0:5]) + sum(IS.loc['interestExpense'][0:5]) + sum(IS.loc['incomeTaxExpense'][0:5]))*(1-0.21)
    #ROC = (sum(IS.loc['netIncome'][0:5]) + sum(IS.loc['interestExpense'][0:5]) + sum(IS.loc['incomeTaxExpense'][0:5]))*(1-0.21) / ((-1)*BS.loc['totalStockholdersEquity'][1]+BS.loc['totalDebt'][1] - BS.loc['cashAndCashEquivalents'][1])
    #expected_growth = reinvestment_rate * ROC
    #print(ROC)
    #print(reinvestment_rate)
    #print(expected_growth)
    #Setter den litt over inflasjonen
    return 0.03


def excpected_free_cash_flow():
    ATOIs = []
    for i in range(0, 5):
        #ATOIs.append(((IS.loc['netIncome'][i]) + sum(IS.loc['interestExpense'][i]) + sum(IS.loc['incomeTaxExpense'][i]))*(1-0.21))
        ATOIs.append(CF.loc["freeCashFlow"][i])
    years = 5
    #print(ATOIs)

    ATOI_growth = []
    discount_rate = WACC()
    ATOI_discount = []
    #print(ATOI_discount)
    vekstrate = []
    #print(vekstrate)

    for i in range(0, years-1):
        vekstrate.append(ATOIs[i]/ATOIs[i+1])

    snitt_vekstrate = sum(vekstrate)/len(vekstrate)
    #print(snitt_vekstrate)
    ny_snitt_vekstrate = (snitt_vekstrate + excpect_growth_rate()) / 2

    #Antagelse om at Apple øker med ca 10% i CAGR hvert år. Går an å sette opp budsjettert, og komme seg fram sånn ca
    #Men per nå er det antagelse om ca 10% i vekst i cashflow. Det stemmer greit historisk sett også
    
    for i in range(0, years):
        ATOI_growth.append(ATOIs[0]*(1.1)**(i+1))
        ATOI_discount.append(ATOI_growth[i]/((1+discount_rate)**(i+1)))
    """print(ATOIs)
    print(ATOI_discount)
    print(ATOI_growth)"""


    return ATOI_discount, ATOI_growth



    """ATOI_growth = []
    reinvestment_income = []
    FCFF = []
    r_rate = 0.17

    # Starting at current year
    ATOI_growth.append(ATOI)
    reinvestment_income.append(None)
    FCFF.append(None)

    for y in range(1,years+1):
        Expected_After_Tax_Operating_Income = ATOI*(1+excpect_growth_rate())**y
        Expected_Reinvestment = r_rate*Expected_After_Tax_Operating_Income
        Expected_FCFF = Expected_After_Tax_Operating_Income - Expected_Reinvestment
        
        ATOI_growth.append(Expected_After_Tax_Operating_Income)
        reinvestment_income.append(Expected_Reinvestment)
        FCFF.append(Expected_FCFF)
    
    Expected_FCFF = pd.DataFrame([ATOI_growth, reinvestment_income, FCFF])
    Expected_FCFF.index = ['After Tax Operating Income', 'Reinvestment','FCFF']
    column_names = []
    for i in Expected_FCFF.columns:
        if i == 0:
            column_names.append('Current Year')
        else:
            column_names.append('Expected Year ' + str(i))
    Expected_FCFF.columns = column_names
    return Expected_FCFF """


def calculate_terminal_value():
    
    """if 0.03 < WACC():
        stable_reinvestment_rate = 0.03 / WACC()
        
        TV_ATOI = excpected_free_cash_flow().iloc[0,-1] * (1 + 0.03)
        
        TV_Reinvestment = TV_ATOI * stable_reinvestment_rate
        
        FCFF_Final = TV_ATOI - TV_Reinvestment
       
        TV = FCFF_Final / (WACC() - 0.03) # wher
           
        Terminal_Value = (TV / (1 + WACC())**(len(excpected_free_cash_flow().columns) - 1))
        print('Used Gordons way of calculating Terminal Value')
        return(Terminal_Value)
    else:
        print('Used Relative Terminal Value')
        Terminal_Value = (float(IM.loc['Software (System & Application)']['EV/EBIT'][0]) * excpected_free_cash_flow().iloc[2,-1]) /(1+WACC())**number_years
        return(Terminal_Value)"""
    ATOI= excpected_free_cash_flow()[1]
    siste_FFCF = ATOI[4]
    Terminal_Value = (siste_FFCF*(1+excpect_growth_rate()))/(WACC()-excpect_growth_rate())
    return Terminal_Value


    #print(IS.loc['netIncome'][0:5])
    #cost_of_equity()
    ##WACC()



pv_terminal_value = calculate_terminal_value() / ((1 + WACC())**5)
enterprise_value = pv_terminal_value + sum(excpected_free_cash_flow()[0])
#print("Hei")
#print(enterprise_value)
#print(sum(excpected_free_cash_flow()[0]))
equity_value = enterprise_value - BS.loc['totalDebt'][0]
#print(equity_value)
num_shares = fs.get_quote(tick, key).loc['sharesOutstanding'][0]
rating = equity_value / num_shares
#print(rating)

"""if __name__ == "__main__":
    Terminal_Value = calculate_terminal_value(5)
    PV_FCFF = 0
    for i in range(1,excpected_free_cash_flow().shape[1]):
        PV_FCFF += excpected_free_cash_flow().loc['FCFF'][i] / (1 + WACC())**(i)
    print('PV_FCFF:', PV_FCFF, 'or',PV_FCFF/1000000000,'billion')
    Value_Operating_Assets = PV_FCFF + Terminal_Value
    Value_Of_Firm = Value_Operating_Assets + BS.loc['cashAndCashEquivalents'][0]
    Value_Of_Equity = Value_Of_Firm - BS.loc['totalDebt'][0]
    num_shares = fs.get_quote(tick, key).loc['sharesOutstanding'][0]
    rating = Value_Of_Firm / num_shares
    print(rating)"""
