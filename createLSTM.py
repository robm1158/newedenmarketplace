import pandas as pd
import utilities
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.layers import LSTM
# from tensorflow.keras.layers import Dropout
# from tensorflow.keras.callbacks import EarlyStopping
# from tensorflow.keras.layers import *

import sklearn as sk
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import TimeSeriesSplit


pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 17)
pd.set_option('display.width', 250)

def lstm_split(data,steps):
    X,y = [],[]
    for i in range(len(data)-steps+1):
        X.append(data[i:(i+steps),:-1])
        y.append(data[(i+steps-1),-1])
    return np.array(X),np.array(y)


data = pd.read_csv("D:\\Code\\eve-aws\\merged-PLAGIOCLASE-PLAGIOCLASE-the-forge-historical-market-orders-2021-06-19_23-30-02.v3.csv.bz2")
data = utilities.convertFromZuluTime(data)
print(data)
# data.plot(x='issued', y='price', kind='scatter')
data = utilities.removeOutliers(data,3)
# print(data)
# data.plot(x='issued', y='price', kind='scatter')
# plt.show()


targetY = data['price']
xFeat = data.iloc[:,3:7]
sc =StandardScaler()
X_ft = sc.fit_transform(xFeat.values)
X_ft = pd.DataFrame(X_ft, index=xFeat.index, columns=xFeat.columns)

X1,y1 = lstm_split(X_ft.values,20)
trainSplit = 0.8
splitIDX = int(np.ceil(len(X1)*trainSplit))
dateIndex = X_ft.index
XTrain, xTest = X1[:splitIDX], X1[splitIDX:]
yTrain, yTest = y1[:splitIDX], y1[splitIDX:]
XTrainDates, xTestDates = dateIndex[:splitIDX], dateIndex[splitIDX:]
print(X1.shape,XTrain.shape,xTest.shape,yTest.shape)

lstm = tf.keras.models.Sequential()
lstm.add(tf.keras.layers.LSTM(50,return_sequences=True,input_shape=(XTrain.shape[1],XTrain.shape[2]),activation='relu'))
# lstm.add(tf.keras.layers.LSTM(50,activation='relu'))
lstm.add(tf.keras.layers.Dense(1))
# lstm.add(tf.keras.layers.Dropout(0.2))
lstm.compile(loss='mean_squared_error',optimizer='adam')
lstm.summary()

history = lstm.fit(XTrain,yTrain,epochs=300,batch_size=4,shuffle=False)
loss = lstm.evaluate(xTest,yTest,verbose=0)

y_predict = lstm.predict(xTest)

print(history.history.keys())
plt.plot(history.history['loss'])
plt.title('loss')
plt.ylabel('loss')
plt.xlabel('epoch')


plt.plot(y_predict,label='predicted')
plt.plot(loss)
plt.show()
