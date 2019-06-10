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
from sklearn.linear_model import Ridge, LinearRegression
def train_linear_regression(X, Y, Xall, Yall):
    X = (X - np.mean(Xall, axis = 0)) / np.std(Xall, axis = 0)
    clf = Ridge(alpha = 1)
    clf.fit(X, Y)
    #print('training:')
    #print('L2 error:\t', np.sum((clf.predict(X) - Y) ** 2) / Y.shape[0])
    #print('score:\t', clf.score(X, Y))
    #print('validation:')
    #print('L2 error:\t', np.sum((clf.predict(Xval) - Yval) ** 2) / Yval.shape[0])
    #print('score:\t', clf.score(Xval, Yval))
    r = np.corrcoef(clf.predict(X).reshape(-1), Y.reshape(-1))
    rall = np.corrcoef(clf.predict(Xall).reshape(-1), Yall.reshape(-1))
    #print('\nCorrelated Coefficient:\n', r[0][1], rall[0][1])
    pred = []
    lenx = Xall.shape[0]
    for i in range(n_of_comp):
        Xind = (Xall[lenx //  n_of_comp * i: lenx // n_of_comp * (i + 1)] - np.mean(Xall, axis = 0)) / np.std(Xall, axis = 0)
        pred.append(clf.predict(Xind).reshape(-1))
    print(pred)
    return np.array(pred)
Xall, Yall = get_data(0, n_of_comp)
lenx = Xall.shape[0]
K = 5
pred = np.zeros((n_of_comp, 29))
for i in range(1):
    X, Y = get_data(n_of_comp // K * i, n_of_comp // K * (i + 1))
    pred += train_linear_regression(X, Y, Xall, Yall)
pred /= K
r = [np.corrcoef(pred[i], Yall[lenx // n_of_comp * i: lenx // n_of_comp * (i + 1)].reshape(-1))[0][1] for i in range(n_of_comp)]
np.save('dnn_r.npy', r)