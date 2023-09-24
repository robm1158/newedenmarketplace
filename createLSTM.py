import pandas as pd
import utilities
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import sklearn as sk
import pathlib
from ItemIdEnum import item
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

def createLSTM(item: str, path: pathlib.Path, n_input: int, n_features: int, epochs: int, batch_size: int, save: bool) -> None:

    early_stop = tf.keras.callbacks.EarlyStopping(monitor = 'loss', patience = 5)
    data = pd.read_csv("D:\\Code\\eve-aws\\merged-PLAGIOCLASE-PLAGIOCLASE-the-forge-historical-market-orders-2021-06-19_23-30-02.v3.csv.bz2")
    data = utilities.convertFromZuluTime(data)
    data = utilities.removeOutliers(data,3)


    data = data.drop(columns=['range','universe_id','http_last_modified'])
    data['issued'] = pd.to_datetime(data['issued'],origin='unix',unit='D').astype(np.int64) // 10**9
    date_time = pd.to_datetime(data['issued'])
    data.set_index('issued',inplace=True)
    # data = data.set_index('issued')
    targetY = data['price']
    xFeat = data
    # sns.displot(xFeat['price'])
    # plt.rcParams['figure.figsize'] = [8, 6]
    # qqplot(xFeat['price'], norm, fit=True, line="45")

    # plt.show()
    sc =StandardScaler()
    X_ft = sc.fit_transform(xFeat.values)
    X_ft = pd.DataFrame(X_ft, index=xFeat.index, columns=xFeat.columns)

    n_input = n_input  

    df_min_model_data = X_ft['price']

    X, y = Sequential_Input_LSTM(df_min_model_data, n_input)
    trainSplit = 0.8
    splitIDX = int(np.floor(len(X)*trainSplit))
    dateIndex = date_time
    XTrain, xTest = X[:splitIDX], X[splitIDX:]
    yTrain, yTest = y[:splitIDX], y[splitIDX:]
    XTrainDates, xTestDates = dateIndex[:splitIDX], dateIndex[splitIDX+10:]


    n_features = n_features

    lstm = tf.keras.models.Sequential()
    lstm.add(tf.keras.layers.InputLayer((n_input,n_features)))
    lstm.add(tf.keras.layers.LSTM(50,return_sequences=True,activation='tanh'))
    lstm.add(tf.keras.layers.Dropout(0.2))
    lstm.add(tf.keras.layers.LSTM(50))
    lstm.add(tf.keras.layers.Dense(50, activation='relu', kernel_initializer='he_normal'))
    lstm.add(tf.keras.layers.Dense(50, activation='relu', kernel_initializer='he_normal'))
    lstm.add(tf.keras.layers.Dense(1))
    lstm.compile(loss='mean_squared_error',optimizer='adam', metrics=tf.keras.metrics.RootMeanSquaredError())
    lstm.summary()

    history = lstm.fit(XTrain,yTrain,epochs=epochs,batch_size=batch_size,shuffle=False,validation_data=(xTest,yTest))
    loss, rmse = lstm.evaluate(xTest,yTest,verbose=0) # type: ignore
    if save == True:
        tf.keras.models.save_model(lstm, f"D:\\Code\\eve-aws\\LSTM_models\\{item}_lstm_model.keras")
    
    print(loss-1,rmse-1)
    test_predictions1 = lstm.predict(xTest).flatten()

    X_test_list = []
    for i in range(len(xTest)):
        X_test_list.append(xTest[i][0])

    # test_predictions1 = test_predictions1[:,n_input-1].flatten()
    
    test_predictions_df1 = pd.DataFrame({'X_test':list(X_test_list), 
                                    'LSTM Prediction':list(test_predictions1)})

    test_predictions_df1.plot(title="LSTM Prediction vs Actual",ylabel='Price')
    plt.show()

    print(history.history.keys())
    
    plt.plot(history.history['loss'],label='loss')
    plt.plot(history.history['val_loss'],label='val_loss')
    plt.title('loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend()
    plt.show()

    plt.plot(history.history['root_mean_squared_error'],label='root_mean_squared_error')
    plt.plot(history.history['val_root_mean_squared_error'],label='val_root_mean_squared_error')
    plt.title('root_mean_squared_error')
    plt.ylabel('root_mean_squared_values')
    plt.xlabel('epoch')
    plt.legend()
    plt.show()

    # plt.scatter(np.array(xTestDates),np.array(X_test_list),label='X_test')
    # plt.scatter(np.array(xTestDates),np.array(test_predictions1),label='LSTM Prediction')
    # plt.title('Estimation of Price')
    # plt.ylabel('Price')
    # plt.xlabel('Dates')
    # plt.legend()
    # plt.show()