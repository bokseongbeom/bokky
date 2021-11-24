import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.pylab import rcParams
rcParams['figure.figsize']=20,10
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM,Dropout,Dense

from sklearn.preprocessing import MinMaxScaler
import pybithumb as Bithumb

def get_ohlv(ticker,ms,ml):
    df = Bithumb.get_candlestick(ticker) # , chart_intervals="12h")

    df['fluctuation'] = df['open'] / df['open'].shift(1) * 100
    df['transaction'] = df['volume'].shift(1) / df['volume'].shift(2) * 100 - 100
    # df = df[['close']].copy()


    df['ma_s'] = df['close'].rolling(ms).mean().shift(1)
    df['ma_l'] = df['close'].rolling(ml).mean().shift(1)

    cond = (df['ma_s'] > df['ma_l'])
    df['status'] = np.where(cond, 1, 0)
    df_dop_row = df.dropna(axis=0)

    return df_dop_row


df = get_ohlv("BTC",5,20)
print(df)

df["index"]=pd.to_datetime(df.index,format="%Y-%m-%d")
df.index=df['index']

plt.figure(figsize=(16,8))
# plt.plot(df["close"],label='Close Price history')

data=df.sort_index(ascending=True,axis=0)
new_dataset=pd.DataFrame(index=range(0,len(df)),columns=['index','close'])

for i in range(0, len(data)):
    new_dataset["index"][i] = data['index'][i]
    new_dataset["close"][i] = data["close"][i]

scaler=MinMaxScaler(feature_range=(0,1))
new_dataset.index=new_dataset.index
new_dataset.drop("index", axis=1, inplace=True)
final_dataset=new_dataset.values

train_data=final_dataset[0:2000,:]
valid_data=final_dataset[2000:,:]

scaler=MinMaxScaler(feature_range=(0,1))
scaled_data=scaler.fit_transform(final_dataset)

x_train_data,y_train_data=[],[]

for i in range(60,len(train_data)):
    x_train_data.append(scaled_data[i-60:i,0])
    y_train_data.append(scaled_data[i,0])

x_train_data,y_train_data=np.array(x_train_data),np.array(y_train_data)
x_train_data=np.reshape(x_train_data,(x_train_data.shape[0],x_train_data.shape[1],1))

lstm_model=Sequential()
lstm_model.add(LSTM(units=50,return_sequences=True,input_shape=(x_train_data.shape[1],1)))
lstm_model.add(LSTM(units=50))
lstm_model.add(Dense(1))

inputs_data=new_dataset[len(new_dataset)-len(valid_data)-60:].values
inputs_data=inputs_data.reshape(-1,1)
inputs_data=scaler.transform(inputs_data)

lstm_model.compile(loss='mean_squared_error',optimizer='adam')
lstm_model.fit(x_train_data,y_train_data,epochs=1,batch_size=1,verbose=2)

X_test=[]

for i in range(60,inputs_data.shape[0]):
    X_test.append(inputs_data[i-60:i,0])
X_test=np.array(X_test)

X_test=np.reshape(X_test,(X_test.shape[0],X_test.shape[1],1))
predicted_closing_price=lstm_model.predict(X_test)
predicted_closing_price=scaler.inverse_transform(predicted_closing_price)

lstm_model.save("saved_model.h5")

train_data=new_dataset[:2000]
valid_data=new_dataset[2000:]


valid_data = valid_data.copy() ## 복사해서 사용
train_data = train_data.copy()

valid_data['Predictions']=predicted_closing_price

print(train_data["close"], valid_data[['close',"Predictions"]])

#plt.plot(train_data["close"])
plt.plot(valid_data[['close',"Predictions"]])

# df1.plot()
# plt.title("Pandas의 Plot메소드 사용 예")
# plt.xlabel("시간")
# plt.ylabel("Data")
plt.show()
