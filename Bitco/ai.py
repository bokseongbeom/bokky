from pybithumb import Bithumb
import pandas as pd
import numpy as np

def ma_income(df, Ns, Nl):
    df = df[['close']].copy()
    df['ma_s'] = df['close'].rolling(Ns).mean().shift(1)
    df['ma_l'] = df['close'].rolling(Nl).mean().shift(1)
    cond = (df['ma_s'] > df['ma_l'])
    df['status'] = np.where(cond, 1, 0)
    df.iloc[-1, -1] = 0

    # 매수/매도 조건
    매수조건 = (df['status'] == 1) & (df['status'].shift(1) != 1)
    매도조건 = (df['status'] == 0) & (df['status'].shift(1) == 1)

    # 수익률 계산
    수익률 = df.loc[매도조건, 'close'].reset_index(drop=True) / df.loc[매수조건, 'close'].reset_index(drop=True)
    수익률 = 수익률 - 0.002

    allday = len(df)
    df = df[df.status == 1]
    buyday = len(df)
    day = buyday / allday

    k = 수익률.cumprod().iloc[-1] / day

    return k

def ma_long_ma_short(df):
    best = pd.DataFrame(columns=['short', 'long', 'result'])

    for i in range(2, 17):
        for j in range(30, 61):
            k = ma_income(df, i, j)
            new_data = {
                'short': i,
                'long': j,
                'result': k
            }
            best = best.append(new_data, ignore_index=True)

    best = best.sort_values('result', ascending=False)
    short = int(best.iloc[0]['short'])
    long = int(best.iloc[0]['long'])

    result = int(best.iloc[0]['result'])

    return short, long, result

def get_ohlv_MA(ticker):
    df = Bithumb.get_candlestick(ticker, chart_intervals="12h")

    return df


searchMA = pd.DataFrame(columns=['Ticker','MAS','MAL','result'])

for coin in Bithumb.get_tickers():
    f = open("BestMa.txt", 'r')
    try:
        df = get_ohlv_MA(coin)

        short, long, result = ma_long_ma_short(df)
        # get_ohlv(coin, short, long)

        new_data = {
            'Ticker': coin,
            'MAS': short,
            'MAL': long,
            'result': result
        }
        searchMA = searchMA.append(new_data, ignore_index=True)

        print(new_data)
        # data = f"Ticker : {coin} MAS : {short} MAL : {long} \n"

    except:
        pass

df_sorted_by_values = searchMA.sort_values(by='result' ,ascending=False)
df_sorted_by_values = df_sorted_by_values[df_sorted_by_values.result > 5]
df_sorted_by_values.to_csv('BestMa.txt')
f.close()