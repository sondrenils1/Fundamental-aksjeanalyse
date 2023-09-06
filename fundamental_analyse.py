import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import web_finans as fs
import dfc_aker as dfc
import dividende_analysis as da
import multiple_analysis as ma


tick = "AAPL"
key = "Your API key. FinancialModelinPrep.com"
apple = yf.Ticker("AAPL")


latest_price = apple.history(period="1d")["Close"].iloc[0]



aksjeverdi_nå = round(latest_price, 2)
testmetode_2 = round(dfc.rating, 2)
testmetode_3 = round(ma.gjennomsnittlig_pris, 2)
testmetode_4 = round(da.dividende_resultat, 2)


vekt_2 = 0.6
vekt_3 = 0.3
vekt_4 = 0.1

vektet_gjennomsnitt = round((testmetode_2 * vekt_2 + testmetode_3 * vekt_3 + testmetode_4 * vekt_4) / (vekt_2 + vekt_3 + vekt_4), 2)

reference_color = '#1f77b4'
reference_value = 190


red_color = '#d62728'
green_color = 'green'


farge_verdi = {
    'aksjeverdi_nå': aksjeverdi_nå,
    'testmetode_2': testmetode_2,
    'testmetode_3': testmetode_3,
    'testmetode_4': testmetode_4,
    'vektet_gjennomsnitt': vektet_gjennomsnitt
}


colored_farge_verdi = {}

for key, value in farge_verdi.items():
    if value < reference_value - 3 and value > 60:
      
        alpha = (reference_value - value) / reference_value 
        color = '#{:02X}{:02X}{:02X}'.format(
            int((1 - alpha) * 255) + 20,
            int((1 - alpha) * 255) - 30,
            50
        )
    elif value < 80:
        color = red_color
    elif value > reference_value + 3:
        
        alpha = (value - reference_value) / (255 - reference_value)
        color = '#{:02X}{:02X}{:02X}'.format(
            255,
            int((1 - alpha) * 255),
            0
        )
    else:
        
        color = reference_color

    colored_farge_verdi[key] = color
colorr = []

for key, color in colored_farge_verdi.items():
    colorr.append(color)
    print(f"{key}: {color}")
print(colorr)


plt.style.use('seaborn-darkgrid')
colors = ['#1f77b4', '#d62728', '#d62728', '#d62728', '#d62728']



fig, ax = plt.subplots()


labels = ['Aksjeverdi Apple nå', 'DCF-analyse', 'Multiple-analyse', 'Dividende-analyse', 'Vektet Gjennomsnitt']
verdier = [aksjeverdi_nå, testmetode_2, testmetode_3, testmetode_4, vektet_gjennomsnitt]
x = np.arange(len(labels))
ax.bar(x, verdier, color=colorr)


for i, v in enumerate(verdier):
    ax.text(i, v + 1, str(v), ha='center', va='bottom')

ax.set_xticks(x)
ax.set_xticklabels(labels)


plt.title('Verdier', fontsize=14)
plt.xlabel('Kategorier', fontsize=12)

ax.yaxis.grid(True, linestyle='--', alpha=0.6)


fig.set_size_inches(10, 6)


plt.show()
