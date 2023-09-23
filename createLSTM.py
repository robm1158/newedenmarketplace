import pandas as pd
import utilities
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import sklearn as sk
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import TimeSeriesSplit
import seaborn as sns
from statsmodels.graphics.gofplots import qqplot
from scipy.stats import norm, uniform


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

data = data.drop(columns=['range','universe_id','http_last_modified'])
print(data)
data['issued'] = pd.to_datetime(data['issued'])
# print(data)
date_time = pd.to_datetime(data['issued'], format='%d.%m.%Y %H:%M:%S').unique()
# data = data.set_index('issued')
targetY = data['price']
xFeat = data.iloc[:,3:12]
print(xFeat)
sns.displot(xFeat['price'])
plt.rcParams['figure.figsize'] = [8, 6]
qqplot(xFeat['price'], norm, fit=True, line="45")

plt.show()
# sc =StandardScaler()
# X_ft = sc.fit_transform(xFeat.values)
# X_ft = pd.DataFrame(X_ft, index=xFeat.index, columns=xFeat.columns)

X1,y1 = lstm_split(xFeat.values,10)
trainSplit = 0.8
splitIDX = int(np.ceil(len(X1)*trainSplit))
dateIndex = xFeat.index
XTrain, xTest = X1[:splitIDX], X1[splitIDX:]
yTrain, yTest = y1[:splitIDX], y1[splitIDX:]
XTrainDates, xTestDates = dateIndex[:splitIDX], dateIndex[splitIDX:]
print(XTrain.shape,xTest.shape,yTrain.shape, yTest.shape)

# lstm = tf.keras.models.Sequential()
# lstm.add(tf.keras.layers.LSTM(50,return_sequences=True,input_shape=(XTrain.shape[1],XTrain.shape[2]),activation='relu'))
# lstm.add(tf.keras.layers.Dense(50, activation='relu', kernel_initializer='he_normal'))
# lstm.add(tf.keras.layers.Dense(50, activation='relu', kernel_initializer='he_normal'))
# lstm.add(tf.keras.layers.Dense(1))
# lstm.add(tf.keras.layers.Dropout(0.5))
# lstm.compile(loss='mean_squared_error',optimizer='adam', metrics='accuracy')
# lstm.summary()

# history = lstm.fit(XTrain,yTrain,epochs=20,batch_size=2,shuffle=False,validation_data=(xTest,yTest))
# loss, acc = lstm.evaluate(xTest,yTest,verbose=0)
# print('Loss: %.3f, Acc: %.3f' % (loss, acc))

# y_predict = lstm.predict(xTest)
# X_test_list = []
# for i in range(len(xTest)):
#     X_test_list.append(xTest[i][0])
    
# print(len(y_predict),len(X_test_list))
# test_predictions_df1 = pd.DataFrame({'x_test':list(X_test_list),
#                                      'LSTM':list(y_predict.flatten())})
# print(test_predictions_df1.head())
# test_predictions_df1.plot()
# print(XTrain.shape,xTest.shape,yTrain.shape, yTest.shape)
# print(len(xTest[0]))
# print(yTest.shape)
# print(len(yTest[0]))
# print(len(targetY))
# # plt.plot(y_predict[0],label='prediction')
# plt.plot(xTest,yTest,label='actual')
# plt.title('prediction')
# plt.ylabel('prediction')
# plt.xlabel('epoch')
# plt.legend()
plt.show()

# print(history.history.keys())
# plt.plot(history.history['loss'],label='loss')
# plt.plot(history.history['val_loss'],label='val_loss')
# plt.title('loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend()

# # tf.keras.utils.plot_model(lstm, to_file='model.png', show_shapes=True, show_layer_names=True)

# # plt.plot(y_predict,label='predicted')
# # plt.plot(loss)
# plt.show()
# print(history.history.keys())
# plt.plot(history.history['accuracy'],label='accuracy')
# plt.plot(history.history['val_accuracy'],label='val_accuracy')
# plt.title('loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend()
# plt.show()
