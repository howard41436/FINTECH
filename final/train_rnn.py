import pickle
import os
with open('dic.pkl', 'rb') as f:
    dic = pickle.load(f)
n_of_comp = 135
import numpy as np
def get_data(st, ed):
    X, Y = [], []
    companies = list(dic.keys())
    for comp in companies[st : ed]:
        for i in range(len(dic[comp]['sentiment_list']) - 1):
            X.append(dic[comp]['sentiment_list'][i])
            Y.append([dic[comp]['return_rate'][i]])
    X, Y = np.array(X), np.array(Y)
    return X, Y
import numpy as np
from keras import regularizers
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout, Activation
from keras.layers import Conv2D, MaxPooling2D, Flatten, LSTM
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
def train_rnn(X, Y, Xall, Yall):
    X = (X - np.mean(Xall, axis = 0)) / np.std(Xall, axis = 0)
    X = X.reshape((X.shape[0] // 29, 29, X.shape[1]))
    Y = Y.reshape((Y.shape[0] // 29, 29))
    model = Sequential()
    model.add(LSTM(128, input_shape = (X.shape[1], X.shape[2])))
    model.add(Dense(29))
    model.compile(loss = 'mse', optimizer = Adam(), metrics = [])
    model.fit(X, Y, batch_size = 32, epochs = 50)
    pred = []
    for i in range(n_of_comp):
        Xind = (Xall[lenx //  n_of_comp * i: lenx // n_of_comp * (i + 1)] - np.mean(Xall, axis = 0)) / np.std(Xall, axis = 0)
        Xind = Xind.reshape((Xind.shape[0] // 29, 29, Xind.shape[1]))
        tmp = model.predict(Xind).reshape(-1)
        pred.append(tmp)
    return np.array(pred)
Xall, Yall = get_data(0, n_of_comp)
lenx = Xall.shape[0]
K = 5
pred = np.zeros((n_of_comp, 29))
for i in range(K):
    X, Y = get_data(n_of_comp // K * i, n_of_comp // K * (i + 1))
    pred += train_rnn(X, Y, Xall, Yall)
pred /= K
np.save('rnn_pred.npy', pred)
r = [np.corrcoef(pred[i], Yall[lenx // n_of_comp * i: lenx // n_of_comp * (i + 1)].reshape(-1))[0][1] for i in range(n_of_comp)]
np.save('rnn_r.npy', r)