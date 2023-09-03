import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf
import web_finans as fs
#import dfc_aker as dfc
#import dividende_analysis as da
#import multiple_analysis as ma
# Hent data for Apple fra Yahoo Finance

tick = "AAPL"
key = "ecd6d371f7dd586779188ceb26f27a72"
apple = yf.Ticker("AAPL")


latest_price = apple.history(period="1d")["Close"].iloc[0]


# Simulerte verdier for aksjeverdien og testmetodene
aksjeverdi_nå = 189 #latest_price
testmetode_2 = 200 #dfc.rating
testmetode_3 = 180# ma.gjennomsnittlig_pris
testmetode_4 = 20 #da.dividende_resultat

# Beregning av vektede verdier
vekt_2 = 0.6
vekt_3 = 0.3
vekt_4 = 0.1

vektet_gjennomsnitt = (testmetode_2 * vekt_2 + testmetode_3 * vekt_3 + testmetode_4 * vekt_4) / (vekt_2 + vekt_3 + vekt_4)

# Tilpass plottet med en annen stil og farger
plt.style.use('seaborn-darkgrid')
colors = ['#1f77b4', '#2ca02c', '#d62728', '#d62728', '#d62728']

# Opprett en figur og aksene for plottet
fig, ax = plt.subplots()

# Lag et stolpediagram for verdiene
labels = ['Aksjeverdi Apple nå', 'DCF-analyse', 'Multiple-analyse', 'Dividende-analyse', 'Vektet Gjennomsnitt']
verdier = [aksjeverdi_nå, testmetode_2, testmetode_3, testmetode_4, vektet_gjennomsnitt]
x = np.arange(len(labels))
ax.bar(x, verdier, color=colors)

# Legg til verdier på stolpene
for i, v in enumerate(verdier):
    ax.text(i, v + 1, str(v), ha='center', va='bottom')

# Sett etiketter for x-aksen
ax.set_xticks(x)
ax.set_xticklabels(labels)

# Legg til en tittel og aksjelabel
plt.title('Verdier', fontsize=14)
plt.xlabel('Kategorier', fontsize=12)

# Legg til en rutenett
ax.yaxis.grid(True, linestyle='--', alpha=0.6)

# Vis plottet med en større størrelse
fig.set_size_inches(10, 6)

# Lagre plottet som en bildefil hvis nødvendig
# plt.savefig('fancy_plot.png', dpi=300, bbox_inches='tight')

# Vis plottet
plt.show()