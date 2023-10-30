import pandas as pd
import utils
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import sklearn as sk
import pathlib
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.model_selection import train_test_split
from sklearn.model_selection import TimeSeriesSplit
import seaborn as sns
from statsmodels.graphics.gofplots import qqplot
from scipy.stats import norm, uniform
from keras import backend as K
from tensorflow_addons.metrics import RSquare
from keras.regularizers import l2


pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', 17)
pd.set_option('display.width', 250)

def coeff_determination(y_true, y_pred):
    SS_res =  K.sum(K.square( y_true-y_pred )) 
    SS_tot = K.sum(K.square( y_true - K.mean(y_true) ) ) 
    return ( 1 - SS_res/(SS_tot + K.epsilon()) )

def Sequential_Input_LSTM(df, input_sequence):
    if isinstance(df, np.ndarray):
        df_np = df
    else:
        df_np = df.to_numpy()
    X = []
    y = []
    
    for i in range(len(df_np) - input_sequence):
        row = [a for a in df_np[i:i + input_sequence]]
        X.append(row)
        label = df_np[i + input_sequence]
        y.append(label)
        
    return np.array(X), np.array(y)

def multi_feature_sequential_input(df, n_input):
    X, y = [], []
    for i in range(len(df) - n_input):
        seq = df[i:i + n_input].values  # This will fetch n_input rows (i.e., a sequence)
        X.append(seq[:-1])  # All rows except last one
        y.append(seq[-1][0])  # Last row, 'average' value
    return np.array(X), np.array(y)


def createLSTM(itemName: str, data: pd.DataFrame, n_input: int, n_features: int, epochs: int, batch_size: int, save: bool, savePlot: bool) -> None:
    cwd = pathlib.Path().cwd()
    path = cwd.joinpath("LSTM_models/"+itemName)
    try:
        path.mkdir(mode=0o777,parents=True, exist_ok=False)
    except FileExistsError as e:
        print(e)
        pass
    
    early_stop = tf.keras.callbacks.EarlyStopping(monitor = 'loss', patience = 5)
    data = utils.convertFromZuluTime(data)
    data = utils.removeOutliers(data)

    data = data.drop(columns=['range','universe_id','http_last_modified'])
    data['issued'] = pd.to_datetime(data['issued'],origin='unix',unit='D')
    date_time = pd.to_datetime(data['issued'])
    data.set_index('issued',inplace=True)
    plt.figure()
    data['price'].hist()
    plt.savefig(f'{path/itemName}_predata_standarize_hist.png')
    plt.clf()
    plt.figure()
    data['price'].plot(ylabel='Price')
    plt.savefig(f'{path/itemName}_predata_standarize_plot.png')
    plt.clf()
    xFeat = data
    sc =MinMaxScaler()
    X_ft = sc.fit_transform(xFeat.values)
    X_ft = pd.DataFrame(X_ft, index=xFeat.index, columns=xFeat.columns)
    plt.figure()
    data['price'].hist()
    plt.savefig(f'{path/itemName}_postdata_standarize_hist.png')
    plt.clf()
    plt.figure()
    data['price'].plot()
    plt.savefig(f'{path/itemName}_postdata_standarize_plot.png')
    plt.clf()
    n_input = n_input  

    df_min_model_data = X_ft['price']

    X, y = Sequential_Input_LSTM(df_min_model_data, n_input)
    trainSplit = 0.8
    splitIDX = int(np.floor(len(X)*trainSplit))
    dateIndex = date_time
    XTrain, xTest = X[:splitIDX], X[splitIDX:]
    yTrain, yTest = y[:splitIDX], y[splitIDX:]
    XTrainDates, xTestDates = dateIndex[:splitIDX], dateIndex[splitIDX+n_input:]
    
    batchLimiter = len(XTrain[:,0])

    if batchLimiter < 500:
        batch_size = 8
    elif batchLimiter < 2000:
        batch_size = 16
    elif batchLimiter < 5000:
        batch_size = 32
    else:
        batch_size = 64

    n_features = n_features

    lstm = tf.keras.models.Sequential()
    lstm.add(tf.keras.layers.InputLayer((n_input,n_features)))
    lstm.add(tf.keras.layers.LSTM(100,return_sequences=True,activation='tanh'))
    lstm.add(tf.keras.layers.Dropout(0.5))
    lstm.add(tf.keras.layers.LSTM(100,return_sequences=True,activation='tanh'))
    lstm.add(tf.keras.layers.LSTM(50))
    lstm.add(tf.keras.layers.Dense(50, activation='tanh'))
    lstm.add(tf.keras.layers.Dense(1))
    lstm.compile(loss='logcosh',optimizer='adam', metrics=[tf.keras.metrics.RootMeanSquaredError(), RSquare()])
    lstm.summary()

    history = lstm.fit(XTrain,yTrain,epochs=epochs,batch_size=batch_size,shuffle=False,validation_data=(xTest,yTest), callbacks = [early_stop],verbose=1) # type: ignore 
    lstm.evaluate(xTest,yTest,verbose=0) # type: ignore
    if save == True:
        tf.keras.models.save_model(lstm, f"D:\\Code\\eve-aws\\LSTM_models\\{itemName}_lstm_model.keras")
    
    test_predictions1 = lstm.predict(xTest).flatten()
    
    X_test_list = []
    for i in range(len(xTest)):
        X_test_list.append(xTest[i][0])
    
    test_predictions_df1 = pd.DataFrame({'X_test':list(X_test_list), 
                                    'LSTM Prediction':list(test_predictions1)})    
    

    test_predictions_df1.plot(title=f'{itemName} LSTM Prediction vs Actual',ylabel='Price')
    # plt.show()
    print(f'================== {itemName} ==================')
    if savePlot == True:
        plt.figure()
        test_predictions_df1.plot(title=f'{itemName} LSTM Prediction vs Actual',ylabel='Price')
        plt.savefig(f'{path/itemName}_prediction_plot.png')

        print(history.history.keys())
        plt.figure()
        plt.plot(history.history['loss'],label='loss')
        plt.plot(history.history['val_loss'],label='val_loss')
        plt.title('loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend()
        plt.savefig(f'{path/itemName}_loss_plot.png')
        plt.clf()
        plt.figure()
        plt.plot(history.history['r_square'],label='r_square')
        plt.plot(history.history['val_r_square'],label='val_r_square')
        plt.title('r_square')
        plt.ylabel('r_square')
        plt.xlabel('epoch')
        plt.legend()
        plt.savefig(f'{path/itemName}_r_square_plot.png')
        plt.clf()
        plt.figure()
        plt.plot(history.history['root_mean_squared_error'],label='root_mean_squared_error')
        plt.plot(history.history['val_root_mean_squared_error'],label='val_root_mean_squared_error')
        plt.title('root_mean_squared_error')
        plt.ylabel('root_mean_squared_values')
        plt.xlabel('epoch')
        plt.legend()
        plt.savefig(f'{path/itemName}_root_mean_squared_error_plot.png')
        plt.clf()
    plt.close('all')


def rmse_loss(y_true, y_pred):
    return tf.sqrt(tf.reduce_mean(tf.square(y_pred - y_true)))

def createHistoryLSTM(itemName: str, data: pd.DataFrame, n_input: int, n_features: int, epochs: int, batch_size: int, save: bool, savePlot: bool) -> None:
    cwd = pathlib.Path().cwd()
    path = cwd.joinpath("LSTM_models/"+itemName)
    try:
        path.mkdir(mode=0o777,parents=True, exist_ok=False)
    except FileExistsError as e:
        print(e)
        pass
    early_stop = tf.keras.callbacks.EarlyStopping(monitor = 'val_r_square', patience = 50)
    date_time = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)

    plt.figure()
    data['average'].hist()
    plt.savefig(f'{path/itemName}_predata_standarize_hist.png')
    plt.clf()
    plt.figure()
    data['average'].plot(ylabel='average')
    plt.savefig(f'{path/itemName}_predata_standarize_plot.png')
    plt.clf()

    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(data)
    scaled_data = pd.DataFrame(scaled_data, columns=data.columns, index=data.index)
    scaler_avg = MinMaxScaler()
    scaled_data['average'] = scaler_avg.fit_transform(data[['average']])
    # Adjustments end here

    plt.figure()
    scaled_data['average'].hist()
    plt.savefig(f'{path/itemName}_postdata_standarize_hist.png')
    plt.clf()
    plt.figure()
    scaled_data['average'].plot()
    plt.savefig(f'{path/itemName}_postdata_standarize_plot.png')
    plt.clf()

    n_input = n_input  
    X, y = multi_feature_sequential_input(scaled_data, n_input)
    trainSplit = 0.8
    splitIDX = int(np.floor(len(X) * trainSplit))
    XTrain, xTest = X[:splitIDX], X[splitIDX:]
    yTrain, yTest = y[:splitIDX], y[splitIDX:]
    dateIndex = date_time
    XTrainDates, xTestDates = dateIndex[:splitIDX], dateIndex[splitIDX+n_input:]

    batchLimiter = len(XTrain[:,0])
    # if batchLimiter < 800:
    #     batch_size = 16
    # elif batchLimiter < 2000:
    #     batch_size = 16
    # elif batchLimiter < 5000:
    #     batch_size = 32
    # else:
    #     batch_size = 64

    # n_features = scaled_data.shape[1]
    print(n_features)
    lstm = tf.keras.models.Sequential()
    lstm.add(tf.keras.layers.InputLayer((n_input-1, n_features)))
    lstm.add(tf.keras.layers.LSTM(100, return_sequences=True, activation='tanh'))
    # lstm.add(tf.keras.layers.Dropout(0.1))
    # lstm.add(tf.keras.layers.LSTM(100, return_sequences=True, activation='tanh'))
    # lstm.add(tf.keras.layers.Dropout(0.2))
    lstm.add(tf.keras.layers.LSTM(100))
    lstm.add(tf.keras.layers.Dense(20, activation='tanh'))
    lstm.add(tf.keras.layers.Dense(1))
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0003)
    lstm.compile(loss='logcosh', optimizer=optimizer, metrics=[tf.keras.metrics.RootMeanSquaredError(), RSquare()])
    lstm.summary()

    history = lstm.fit(XTrain, yTrain, epochs=epochs, batch_size=batch_size, shuffle=False, validation_data=(xTest, yTest), callbacks = [early_stop], verbose=1)
    lstm.evaluate(xTest, yTest, verbose=0)
    if save == True:
        tf.keras.models.save_model(lstm, f"D:\\Code\\eve-aws\\LSTM_models\\{itemName}_lstm_model.keras")

    test_predictions1 = lstm.predict(xTest).flatten()
    test_predictions1_original = scaler_avg.inverse_transform(test_predictions1.reshape(-1, 1)).flatten()
    yTest_original = scaler_avg.inverse_transform(yTest.reshape(-1, 1)).flatten()


    # X_test_list = []
    # for i in range(len(xTest)):
    #     X_test_list.append(xTest[i][0])
    test_predictions_df1 = pd.DataFrame({'Actual': list(yTest_original), 'LSTM Prediction': list(test_predictions1_original)})
    test_predictions_df1.index = xTestDates
    test_predictions_df1.plot(title=f'{itemName} LSTM Prediction vs Actual', ylabel='average')
    # plt.show()

    print(f'================== {itemName} ==================')
    if savePlot == True:
        mean_loss = history.history['loss'][-1]
        mean_val_loss = history.history['val_loss'][-1]
        mean_r_square = history.history['r_square'][-1]
        mean_val_r_square = history.history['val_r_square'][-1]
        
        plt.figure()
        test_predictions_df1.plot(title=f'{itemName} LSTM Prediction vs Actual', ylabel='average')
        plt.savefig(f'{path/itemName}_prediction_plot.png')

        print(history.history.keys())
        plt.figure()
        plt.plot(history.history['loss'],label='loss')
        plt.plot(history.history['val_loss'],label='val_loss')
        plt.title('loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend()
        plt.text(1, 0.50, f'Mean Loss: {mean_loss:.4f}', horizontalalignment='right', verticalalignment='center', transform=plt.gca().transAxes)
        plt.text(1, 0.55, f'Mean Val Loss: {mean_val_loss:.4f}', horizontalalignment='right', verticalalignment='center', transform=plt.gca().transAxes)
        plt.savefig(f'{path/itemName}_loss_plot.png')
        plt.clf()
        plt.figure()
        plt.plot(history.history['r_square'],label='r_square')
        plt.plot(history.history['val_r_square'],label='val_r_square')
        plt.ylim(0, 1)
        plt.title('r_square')
        plt.ylabel('r_square')
        plt.xlabel('epoch')
        plt.legend()
        plt.text(1, 0.50, f'Mean Loss: {mean_r_square:.4f}', horizontalalignment='right', verticalalignment='center', transform=plt.gca().transAxes)
        plt.text(1, 0.55, f'Mean Val Loss: {mean_val_r_square:.4f}', horizontalalignment='right', verticalalignment='center', transform=plt.gca().transAxes)
        plt.savefig(f'{path/itemName}_r_square_plot.png')
        plt.clf()
        plt.figure()
        plt.plot(history.history['root_mean_squared_error'],label='root_mean_squared_error')
        plt.plot(history.history['val_root_mean_squared_error'],label='val_root_mean_squared_error')
        plt.title('root_mean_squared_error')
        plt.ylabel('root_mean_squared_values')
        plt.xlabel('epoch')
        plt.legend()
        plt.savefig(f'{path/itemName}_root_mean_squared_error_plot.png')
        plt.clf()
    plt.close('all')

    