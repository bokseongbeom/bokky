import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


import pandas as pd
import pybithumb as Bithumb
import numpy as np
import datetime
import time

print("pandas version: ", pd.__version__)
pd.set_option('display.max_row', 500)
pd.set_option('display.max_columns', 100)

f = open("bithumb.txt", 'r')
lines = f.readlines()
apiKey = lines[0].strip()
secKey = lines[1].strip()
f.close()

bithumb = Bithumb.Bithumb(apiKey, secKey)

df = pd.read_table('BestMa.txt', sep=',')


def Split_purchase(df):
    total = 0
    for idx in range(len(df[:3])):
        Ticker = df.Ticker.values[idx]
        abc = int(df.result.loc[df['Ticker'] == Ticker])
        total = total + abc

    print(total)

    importances = []

    for idx in range(len(df[:3])):
        Ticker = df.Ticker.values[idx]
        abc = int(df.result.loc[df['Ticker'] == Ticker])
        importanced = abc/total
        importances.append(round(importanced,1))
        print(importances[idx])

    krw = bithumb.get_balance("BTC")[2]

    for idx in range(3):
        krwXticker = krw * importances[idx]
        print(importances[idx], df.Ticker.values[idx], krwXticker)
        buy_crypto_currencyA(bithumb, ticker, krwXticker)

    return True

def get_ohlv(ticker,ms,ml):
    df = Bithumb.get_candlestick(ticker, chart_intervals="12h")

    df['fluctuation'] = df['open'] / df['open'].shift(1) * 100 -100
    df['transaction'] = df['volume'].shift(1) / df['volume'].shift(2) * 100 - 100
    # df = df[['close']].copy()


    df['ma_s'] = df['close'].rolling(ms).mean().shift(1)
    df['ma_l'] = df['close'].rolling(ml).mean().shift(1)

    cond = (df['ma_s'] > df['ma_l'])
    df['status'] = np.where(cond, 1, 0)

    return df


df = get_ohlv("BTC",5,20)

plt.figure(figsize=(7,4))

plt.title('BTC close')
plt.ylabel('price(won)')
plt.xlabel('period(day)')
plt.grid()

plt.plot(df['transaction'], label='fluctuation', color='b')
plt.legend(loc='best')

plt.show()