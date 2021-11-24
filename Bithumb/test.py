import pandas as pd
import pybithumb as Bithumb
import numpy as np
import datetime
import time
import math


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
    unit = math.floor(unit * 10000) / 10000
    return bithumb.buy_market_order(ticker, unit)

def get_ohlv(ticker,ms,ml):
    df = Bithumb.get_candlestick(ticker, chart_intervals="12h")
    df = df[['close']].copy()
    df['ma_s'] = df['close'].rolling(ms).mean().shift(1)
    df['ma_l'] = df['close'].rolling(ml).mean().shift(1)
    cond = (df['ma_s'] > df['ma_l'])
    df['status'] = np.where(cond, 1, 0)

    if (df['status'][-2] == 0) & (df['status'][-1] == 1):
        #print('지금이니', df['ma_s'][-1])
        return "지금이니", df['ma_s'][-1]
    elif (df['status'][-2] == 1) & (df['status'][-1] == 0):
        #print('팔아!', df['ma_s'][-1])
        return "팔아!", df['ma_s'][-1]
    elif (df['status'][-2] == 1) & (df['status'][-1] == 1):
        #print('홀딩해', df['ma_s'][-1])
        return "홀딩해", df['ma_s'][-1]
    elif (df['status'][-2] == 0) & (df['status'][-1] == 0):
        #print('도망쳐', df['ma_s'][-1])
        return "도망쳐", df['ma_s'][-1]

def buy_crypto_currencyA(bithumb, ticker, krw, start):
    orderbook = Bithumb.get_orderbook(ticker)
    sell_price = orderbook['asks'][0]['price']
    unit = krw / float(sell_price) * 0.7
    unit = math.floor(unit * 10000) / 10000
    bithumb.buy_market_order(ticker, unit)
    print(ticker, krw, unit)
    start = start + 1
    if start < 3:
        krw = krw * 0.3
        buy_crypto_currencyA(bithumb, ticker, krw, start)
    else:
        pass

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
        print(Ticker, abc)

    krw = bithumb.get_balance("BTC")[2]

    for idx in range(3):
        ticker = df.Ticker.values[idx]
        krwXticker = krw * importances[idx] * 0.7
        print(f"{df.Ticker.values[idx]}를 보유 원화{krw}원 중 {krwXticker}원 만큼 매수")

        buy_crypto_currencyA(bithumb, ticker, krwXticker, 0)


alive = True

while alive:
    df = pd.read_table('BestMa.txt', sep=',')
    buy_coin_list = pd.DataFrame(columns=['Ticker', 'result'])
    try:
        ticker_list = []
        for idx in range(len(df)):
            ticker = df.Ticker.values[idx]
            mas = int(df.MAS.values[idx])
            mal = int(df.MAL.values[idx])

            # print(ticker, mas, mal, Bithumb.get_current_price(ticker))
            position, target_price = get_ohlv(ticker, mas, mal)
            if (position == "지금이니"):
                print(f"{ticker}지금이니!~")
                ticker_list.append(ticker)
                result = df.result.values[idx]

                new_data = {
                    'Ticker': ticker,
                    'result': result,
                }
                buy_coin_list = buy_coin_list.append(new_data, ignore_index=True)

            elif (position == "홀딩해"):
                print(f"{ticker}홀딩해!~")
                ticker_list.append(ticker)
                result = df.result.values[idx]

                new_data = {
                    'Ticker': ticker,
                    'result': result/2,
                }
                buy_coin_list = buy_coin_list.append(new_data, ignore_index=True)
            else:
                #print(f"{ticker}팔아보룟!~")
                sell_crypto_currency(bithumb, ticker)
                bithumb.get_balance(ticker)[0]
        print("포트폴리오구성")

        print(buy_coin_list)

        krw = bithumb.get_balance("BTC")[2]

        if krw > 100000:
            print("분 할매 수 시쟉~")
            print(buy_coin_list)
            Split_purchase(buy_coin_list)
        else:
            print("so sad~")
            # ticker = buy_coin_list.Ticker[0]
            # if krw > 10000:
            #     #buy_crypto_currency(bithumb, ticker)
            #     print(f"{ticker}를 보유 원화{krw} 중 70% 만큼 매수")

    except:
        pass
    time.sleep(10)