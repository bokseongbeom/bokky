import pandas as pd
import pybithumb as Bithumb
import numpy as np
import datetime
import time

df = pd.read_table('BestMa.txt', sep=',')

f = open("bithumb.txt", 'r')
lines = f.readlines()
apiKey = lines[0].strip()
secKey = lines[1].strip()
f.close()



bithumb = Bithumb.Bithumb(apiKey, secKey)

def sell_crypto_currency(bithumb, ticker):
    unit = bithumb.get_balance(ticker)[0]
    return bithumb.sell_market_order(ticker, unit)

def buy_crypto_currency(bithumb, ticker):
    krw = bithumb.get_balance(ticker)[2]
    orderbook = Bithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = krw / float(sell_price) * 0.7
    return bithumb.buy_market_order(ticker, unit)

def get_ohlv(ticker,ms,ml):
    df = Bithumb.get_candlestick(ticker, chart_intervals="12h")
    df = df[['close']].copy()
    df['ma_s'] = df['close'].rolling(ms).mean().shift(1)
    df['ma_l'] = df['close'].rolling(ml).mean().shift(1)
    cond = (df['ma_s'] > df['ma_l'])
    df['status'] = np.where(cond, 1, 0)

    if (df['status'][-2] == 0) & (df['status'][-1] == 1):
        print('지금이니', df['ma_s'][-1])
        return "지금이니", df['ma_s'][-1]
    elif (df['status'][-2] == 1) & (df['status'][-1] == 0):
        print('팔아!', df['ma_s'][-1])
        return "팔아!", df['ma_s'][-1]
    elif (df['status'][-2] == 1) & (df['status'][-1] == 1):
        print('홀딩해', df['ma_s'][-1])
        return "홀딩해", df['ma_s'][-1]
    elif (df['status'][-2] == 0) & (df['status'][-1] == 0):
        print('도망쳐', df['ma_s'][-1])
        return "도망쳐", df['ma_s'][-1]


alive = True
get_coin_list = pd.DataFrame(columns=['Ticker','target_price','MAL'])
while alive:
    try:
        for idx in range(len(df)):
            ticker = df.Ticker.values[idx]
            mas = int(df.MAS.values[idx])
            mal = int(df.MAL.values[idx])

            print(ticker, mas, mal, Bithumb.get_current_price(ticker))
            position, target_price = get_ohlv(ticker, mas, mal)
            if (position == "지금이니"):
                if bithumb.get_balance(ticker)[2] > 5000:
                    print("매수해쬬옹@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    buy_crypto_currency(bithumb, ticker)
                print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
                # get_coin_list = get_coin_list.append(,)
            elif (position == "홀딩해"):
                print("나중에봐용~")
            else:
                print("팔아보룟!~")
                sell_crypto_currency(bithumb, ticker)
                bithumb.get_balance(ticker)[0]

    except:
        pass
    time.sleep(1)