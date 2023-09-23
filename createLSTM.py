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

def Sequential_Input_LSTM(df, input_sequence):
    df_np = df.to_numpy()
    X = []
    y = []
    
    for i in range(len(df_np) - input_sequence):
        row = [a for a in df_np[i:i + input_sequence]]
        X.append(row)
        label = df_np[i + input_sequence]
        y.append(label)
        
    return np.array(X), np.array(y)
early_stop = tf.keras.callbacks.EarlyStopping(monitor = 'loss', patience = 5)
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
date_time = pd.to_datetime(data['issued'], format='%d.%m.%Y %H:%M:%S')
# data = data.set_index('issued')
targetY = data['price']
xFeat = data.iloc[:,3:12]
print(xFeat)
# sns.displot(xFeat['price'])
# plt.rcParams['figure.figsize'] = [8, 6]
# qqplot(xFeat['price'], norm, fit=True, line="45")

# plt.show()
# sc =StandardScaler()
# X_ft = sc.fit_transform(xFeat.values)
# X_ft = pd.DataFrame(X_ft, index=xFeat.index, columns=xFeat.columns)

n_input = 10  

df_min_model_data = xFeat['price']

X, y = Sequential_Input_LSTM(df_min_model_data, n_input)
print(date_time)
trainSplit = 0.8
splitIDX = int(np.floor(len(X)*trainSplit))
dateIndex = date_time
XTrain, xTest = X[:splitIDX], X[splitIDX:]
yTrain, yTest = y[:splitIDX], y[splitIDX:]
XTrainDates, xTestDates = dateIndex[:splitIDX], dateIndex[splitIDX:]
print(XTrain.shape,xTest.shape,yTrain.shape, yTest.shape, XTrainDates.shape, xTestDates.shape)
print(len(XTrain),len(xTest),len(yTrain), len(yTest), len(XTrainDates), len(xTestDates))

n_features = 1

lstm = tf.keras.models.Sequential()
lstm.add(tf.keras.layers.InputLayer((n_input,n_features)))
lstm.add(tf.keras.layers.LSTM(50,return_sequences=True,activation='relu'))
lstm.add(tf.keras.layers.Dense(50, activation='relu', kernel_initializer='he_normal'))
lstm.add(tf.keras.layers.Dense(50, activation='relu', kernel_initializer='he_normal'))
lstm.add(tf.keras.layers.Dense(1))
# lstm.add(tf.keras.layers.Dropout(0.5))
lstm.compile(loss='mean_squared_error',optimizer='adam', metrics='accuracy')
lstm.summary()

history = lstm.fit(XTrain,yTrain,epochs=70,batch_size=2,shuffle=False,validation_data=(xTest,yTest),callbacks = [early_stop])
loss, acc = lstm.evaluate(xTest,yTest,verbose=0)

test_predictions1 = lstm.predict(xTest)
test_predictions1 = test_predictions1[:,0].flatten()
X_test_list = []
for i in range(len(xTest)):
    X_test_list.append(xTest[i][0])
print(len(X_test_list))
print(len(test_predictions1),len(X_test_list))
test_predictions_df1 = pd.DataFrame({'X_test':list(X_test_list), 
                                    'LSTM Prediction':list(test_predictions1)})
print(test_predictions_df1.head())    

test_predictions_df1.plot(title="LSTM Prediction vs Actual")

# print(history.history.keys())
# plt.plot(history.history['loss'],label='loss')
# plt.plot(history.history['val_loss'],label='val_loss')
# plt.title('loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend()
plt.show()

# plt.plot(history.history['accuracy'],label='accuracy')
# plt.plot(history.history['val_accuracy'],label='val_accuracy')
# plt.title('loss')
# plt.ylabel('loss')
# plt.xlabel('epoch')
# plt.legend()
# plt.show()