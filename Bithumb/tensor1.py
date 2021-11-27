import pandas as pd
import numpy as np
import pybithumb as Bithumb
import matplotlib.pyplot as plt
# 생각해바 목표를 잃었잖아 오실레이터 macd
import pybithumb
import requests
import pandas as pd
import time
import datetime  # 거래 이력 데이터프레임에서 timestamp(시간)을 계산하기 위한 모듈 추가

coin_name = input("코인 이름을 입력하세요 : ")
candle_period = input("캔들스틱 주기(단위기간)을 입력하세요 : ")

juso = "https://api.bithumb.com/public/candlestick/{coin}_KRW/{t}".format(coin=coin_name, t=candle_period)


# 캔들스틱 불러오기
def call_data(juso):
    data = requests.get(juso)
    data = data.json()
    data = data.get("data")
    df = pd.DataFrame(data)
    df.rename(columns={0: 'time', 1: "시가", 2: "종가", 3: "고가", 4: "저가", 5: "거래량"}, inplace=True)
    df.sort_values("time", inplace=True)
    df = df.tail(365)
    df = df[['time', "시가", "종가", "고가", "저가", "거래량"]].astype("float")
    df.reset_index(drop=True, inplace=True)
    return df

def call_RSI(df):
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

    # RSI값이 30 이하일 때 매수, 80 이상일 때 매도하도록 설정해보겠습니다.
    # 좀 더 최적화된 값은 다음 시간에 찾아보께요.
    df["RSI_sign"] = df["RSI"].apply(lambda x: "매수" if x < 20 else ("매도" if x > 80 else "대기"))

    return df["RSI_sign"][len(df) - 1], df

def call_MACD(df):
    macd_short, macd_long, macd_signal=12,26,9
    df["MACD_short"]=df["종가"].rolling(macd_short).mean()
    df["MACD_long"]=df["종가"].rolling(macd_long).mean()
    df["MACD"]=df.apply(lambda x: (x["MACD_short"]-x["MACD_long"]), axis=1)
    df["MACD_signal"]=df["MACD"].rolling(macd_signal).mean()
    #df[["MACD_short","MACD_long","MACD","MACD_signal"]].fillna(0, inplace=True)
    df["MACD_sign"]=df.apply(lambda x: ("매수" if x["MACD"]>x["MACD_signal"] else "매도"), axis=1)
    return df["MACD_sign"][len(df)-1],df


def call_stochastic(df):
    # 빗썸 차트를 참고하여 기본값으로 수정했습니다.
    sto_N = 14
    sto_m = 1
    sto_t = 3

    # 스토캐스틱 %K (fast %K) = (현재가격-N일중 최저가)/(N일중 최고가-N일중 최저가) ×100
    df["max%d" % sto_N] = df["고가"].rolling(sto_N).max()  # 오타 수정 : 저가 --> 고가
    df["min%d" % sto_N] = df["저가"].rolling(sto_N).min()
    df["stochastic%K"] = df.apply(lambda x: 100 * (x["종가"] - x["min%d" % sto_N]) /
                                            (x["max%d" % sto_N] - x["min%d" % sto_N])
    if (x["max%d" % sto_N] - x["min%d" % sto_N]) != 0 else 50, 1)

    # 스토캐스틱 %D (fast %D) = m일 동안 %K 평균 = Slow %K
    # slow %K = 위에서 구한 스토캐스틱 %D
    df["slow_%K"] = df["stochastic%K"].rolling(sto_m).mean()

    # slow %D = t일 동안의 slow %K 평균
    df["slow_%D"] = df["slow_%K"].rolling(sto_t).mean()

    # 50일 이동평균선
    df["MA50"] = df["종가"].rolling(50).mean()

    # slow%K선이 slow%D를 골든크로스하고, 현재 종가가 MA50보다 클 때, 매수
    # 반대일 경우, 매도하도록 설정해보겠습니다.

    # df[["max%d"%sto_N,"min%d"%sto_N,"stochastic%K","slow_%K","slow_%D","MA50"]].fillna(0, inplace=True)

    stochastic_sign = []
    try:
        for i in range(len(df)):
            if df.loc[i, "slow_%K"] > df.loc[i, "slow_%D"]:  # and df.loc[i,"종가"]>df.loc[i,"MA50"] 조건 삭제
                if df.loc[i, "slow_%K"] < 20:
                    stochastic_sign.append("대기")
                else:
                    stochastic_sign.append("매수")
            elif df.loc[i, "slow_%K"] < df.loc[i, "slow_%D"]:  # and df.loc[i,"종가"]<df.loc[i,"MA50"] 조건 삭제
                if df.loc[i, "slow_%K"] > 80:
                    stochastic_sign.append("대기")
                else:
                    stochastic_sign.append("매도")
            else:
                stochastic_sign.append("대기")
    except Exception as ex:
        print(i, ex)
    df["stochastic_sign"] = stochastic_sign
    return df["stochastic_sign"][len(df) - 1], df


def call_bb(df):  # 볼린저밴드 함수 추가

    w = 20  # 기준 이동평균일
    k = 2  # 기준 상수

    # 중심선 (MBB) : n일 이동평균선
    df["mbb"] = df["종가"].rolling(w).mean()
    df["MA20_std"] = df["종가"].rolling(w).std()

    # 상한선 (UBB) : 중심선 + (표준편차 × K)
    # 하한선 (LBB) : 중심선 - (표준편차 × K)
    df["ubb"] = df.apply(lambda x: x["mbb"] + k * x["MA20_std"], 1)
    df["lbb"] = df.apply(lambda x: x["mbb"] - k * x["MA20_std"], 1)

    # df[['종가','mbb', 'ubb', 'lbb']][-200:].plot.line()

    # df[["mbb","MA20_std","ubb","lbb"]].fillna(0, inplace=True)

    # 밴드를 이탈했다가 진입할 때 거래
    bb_sign = []
    for i in range(len(df)):
        if i < 20:
            bb_sign.append("대기")
        elif df.loc[i - 1, "종가"] >= df.loc[i - 1, "ubb"] and df.loc[i, "종가"] < df.loc[i, "ubb"]:
            bb_sign.append("매도")
        elif df.loc[i - 1, "종가"] < df.loc[i - 1, "lbb"] and df.loc[i, "종가"] < df.loc[i, "lbb"]:
            bb_sign.append("매수")
        else:
            bb_sign.append("대기")

    df["bb_sign"] = bb_sign

    return df["bb_sign"][len(df) - 1], df


def backtesting(df, method):
    fee = 0.0025
    invest = 1000000
    fig = plt.figure()

    # 수수료율이 0.25%, 초기 투자금이 1백만원인 경우로 테스트하겠습니다.

    for i in range(len(df)):

        if i == 0:
            df.loc[i, "%s_KRW" % method] = invest
            df.loc[i, "%s_coin" % method] = 0
            df.loc[i, "%s_buy" % method] = None
            df.loc[i, "%s_sell" % method] = None
        elif df.loc[i, "%s_sign" % method] == "매수" and df.loc[i - 1, "%s_KRW" % method] > 5000:
            # 보유 현금이 5천원 이상일때 실행
            buy_coin = float(str(round(df.loc[i - 1, "%s_KRW" % method] / df.loc[i, "종가"], 12))[:11])
            buy_unit_fee = buy_coin * (1 - fee)
            df.loc[i, "%s_KRW" % method] = df.loc[i - 1, "%s_KRW" % method] - buy_coin * df.loc[i, "종가"]
            # 매수에 사용된 원화를 빼줌

            df.loc[i, "%s_coin" % method] = df.loc[i - i, "%s_coin" % method] + buy_unit_fee
            # 매수된 코인에서 수수료를 빼고, 보유 코인값에 더해줌

            df.loc[i, "%s_buy" % method] = df.loc[i, "종가"]
            df.loc[i, "%s_sell" % method] = None
        elif df.loc[i, "%s_sign" % method] == "매도" and df.loc[i, "종가"] * df.loc[i - 1, "%s_coin" % method] > 5000:
            # 보유 코인가치가 5천원 이상일때 실행
            sell_coin = df.loc[i - 1, "%s_coin" % method]
            df.loc[i, "%s_KRW" % method] = round((df.loc[i, "종가"] * sell_coin), 4) * (1 - fee) + df.loc[
                i - 1, "%s_KRW" % method]
            df.loc[i, "%s_coin" % method] = df.loc[i - 1, "%s_coin" % method] - sell_coin
            df.loc[i, "%s_buy" % method] = None
            df.loc[i, "%s_sell" % method] = df.loc[i, "종가"]
        else:  # 대기
            df.loc[i, "%s_KRW" % method] = df.loc[i - 1, "%s_KRW" % method]
            df.loc[i, "%s_coin" % method] = df.loc[i - 1, "%s_coin" % method]
            df.loc[i, "%s_buy" % method] = None
            df.loc[i, "%s_sell" % method] = None

    # 백테스팅 결과 수익률, 수익금액 계산
    수익금 = (df.loc[len(df) - 1, "%s_coin" % method] * df.loc[len(df) - 1, "시가"]) \
          + df.loc[len(df) - 1, "%s_KRW" % method] - df.loc[0, "%s_KRW" % method]
    수익률 = 100 * (df.loc[len(df) - 1, "%s_coin" % method] * df.loc[len(df) - 1, "시가"] \
                 + df.loc[len(df) - 1, "%s_KRW" % method]) / df.loc[0, "%s_KRW" % method] - 100
    거래횟수 = len(df[(df["%s_buy" % method] > 0) | (df["%s_sell" % method] > 0)][
                   ["시가", "종가", "%s_buy" % method, "%s_sell" % method]])

    print("{0}일간 백테스팅 결과, {1}만원 투자시 예상수익 : {2}원, 예상수익률 : {3}%, 거래횟수 : {4} ".
          format(len(df), int(invest / 10000), format(int(수익금), ","), format(수익률, '.2f'), 거래횟수))

    return 수익금, 수익률


df = call_data(juso)
result = []
for 보조지표 in ["MACD", "RSI", "stochastic", "bb"]:
    if 보조지표 == "MACD":
        현재상태, df = call_MACD(df)
    elif 보조지표 == "RSI":
        현재상태, df = call_RSI(df)
    elif 보조지표 == "stochastic":
        현재상태, df = call_stochastic(df)
    elif 보조지표 == "bb":
        현재상태, df = call_bb(df)
    else:
        pass
    print("[%s]" % 보조지표, 현재상태)
    result.append([보조지표, backtesting(df, 보조지표)[0]])

### 가장 좋은 성과 지표 선택

max_수익 = 0
for i in result:
    if max_수익 < i[1]:
        max_수익 = i[1]
        select = i[0]
print("가장 좋은 성과가 예상되는 보조지표는 \"%s\"입니다." % select)
