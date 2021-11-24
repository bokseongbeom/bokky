from pybithumb import Bithumb
import pandas as pd
import numpy as np
import pymysql

def get_ohlv(ticker,ms,ml):
    df = Bithumb.get_candlestick(ticker, chart_intervals="12h")
    df = df[['close']].copy()
    df['ma_s'] = df['close'].rolling(ms).mean().shift(1)
    df['ma_l'] = df['close'].rolling(ml).mean().shift(1)
    cond = (df['ma_s'] > df['ma_l'])
    df['status'] = np.where(cond, 1, 0)
    df.iloc[-1, -1] = 0

    if (df['status'][-2] == 0) & (df['status'][-1] == 1):
        return "지금이니"
    elif (df['status'][-2] == 1) & (df['status'][-1] == 0):
        return "팔아!"
    elif (df['status'][-2] == 1) & (df['status'][-1] == 1):
        return "홀딩해"
    elif (df['status'][-2] == 0) & (df['status'][-1] == 0):
        return "도망쳐"

for coin in  Bithumb.get_tickers()[:150]:
    f = open("BestMa.txt", 'r')
    searchMA = pd.DataFrame(columns=['Ticker','MAS','MAL'])

    try:
        df = get_ohlv_MA(coin)

        short, long = ma_long_ma_short(df)
        get_ohlv(coin,short,long)

        new_data = {
            'Ticker': coin,
            'MAS': short,
            'MAL': long
        }
        searchMA.append(new_data, ignore_index=True)

        print(new_data)
        # data = f"Ticker : {coin} MAS : {short} MAL : {long} \n"

    except:
        pass

print(searchMA)
searchMA.to_csv('BestMa.txt')
f.close()