import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import rcParams
import pybithumb as Bithumb


def get_RSI(df):
    # 상승, 하락분을 알기위해 현재 종가에서 전일 종가를 빼서 데이터프레임에 추가하겠습니다.
    RSI_n = 14
    df["등락"] = [df.loc[i, "종가"] - df.loc[i - 1, "종가"] if i > 0 else 0 for i in range(len(df))]
    # i가 0일때는 전일값이 없어서 제외함, i는 데이터프레임의 index값

    # U(up): n일 동안의 종가 상승 분
    df["RSI_U"] = df["등락"].apply(lambda x: x if x > 0 else 0)

    # D(down): n일 동안의 종가 하락 분 --> 음수를 양수로 바꿔줌
    df["RSI_D"] = df["등락"].apply(lambda x: x * (-1) if x < 0 else 0)

    # AU(average ups): U값의 평균
    df["RSI_AU"] = df["RSI_U"].rolling(RSI_n).mean()

    # DU(average downs): D값의 평균
    df["RSI_AD"] = df["RSI_D"].rolling(RSI_n).mean()

    df["RSI"] = df.apply(lambda x: x["RSI_AU"] / (x["RSI_AU"] + x["RSI_AD"]) * 100, 1)

    # df[["등락","RSI_U","RSI_D","RSI_AU","RSI_AD","RSI"]].fillna(0, inplace=True)


def get_ohlv(ticker,ms,ml):
    df = Bithumb.get_candlestick(ticker, chart_intervals="24h")

    df['fluctuation'] = df['high'] / df['open'].shift(1) * 100
    df['transaction'] = df['volume'].shift(1) / df['volume'].shift(2) * 100 - 100
    # df = df[['close']].copy()



    df['ma_s'] = df['close'].rolling(ms).mean().shift(1)
    df['ma_l'] = df['close'].rolling(ml).mean().shift(1)

    k = 101

    macross = (df['ma_s'] > df['ma_l'])
    fluct = (df['fluctuation'] > k)


    df['up'] = np.where(macross, 1, 0)
    df['status'] = np.where(fluct, 1, 0)
    df['after'] = df.status.shift(1)


    df_denominator = df.up.values == 1
    df_molecule = df.status.values == 1
    df_after = df.after.values == 1

    dodo = df[df_denominator & df_molecule]
    ddodod = df[df_denominator]

    popo = df[df_molecule]

    koko = df[df_molecule & df_after & df_denominator]
    kkokko = df[df_after & df_denominator]

    print("suchch", len(popo)/len(df))

    print("super", len(koko)/ len(kkokko))
    print(len(koko)/ len(kkokko) * k)
    print(len(dodo), len(ddodod))
    print(len(dodo)/len(ddodod))


    df_dop_rowtghfy = df.dropna(axis=0)

    return df_dop_rowtghfy


df = get_ohlv("BTC",5,20)
print(df["status"])












