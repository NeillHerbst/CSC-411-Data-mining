# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:12:24 2015

@author: Neill
"""
from __future__ import division
from sklearn import svm
import pandas as pd
import json
import os
import numpy as np

# Retrieve all working directories
with open('config.json') as f:
    config = json.load(f)


def filename(location, pattern):
    return os.path.expanduser(os.path.join(config[location], pattern))


def data_filter(DataFrame, colums):
    df = DataFrame
    df = df[collist]
    for col in colums:
        df = df[np.isfinite(df[col])]
    df = df.reset_index(drop=True)
    return df

# Data path
Dat_path = filename('Data', 'Sample_list_v2.0.xlsx')

# Data file
Dat_file = pd.ExcelFile(Dat_path)
Dat_file = Dat_file.parse('Sample List')

# Dataframe
Df = pd.DataFrame(Dat_file)

# Colums used for SVM
collist = ['Stirrer Time', 'Temp (C)', 'Result']

# Filtering data to remove rows containing empty values
Df = data_filter(Df, collist)

# Fraction of data for training
frac = 0.5

# Calculating Dataframe split position
split = len(Df) * frac

# Data for SVM
x_lst = ['Stirrer Time', 'Temp (C)']
X = Df[x_lst]

x_train = X[X.index <= split]
x_test = X[X.index > split]

Y = Df.Result
y_train = Y[Y.index <= split]
y_test = Y[Y.index > split].values


# Creating SVM
clf = svm.SVC(probability=True)
clf.fit(x_train, y_train)

# Prediction
predict = clf.predict(x_test)

# Accuracy
n = 0
tot = 0
for i, y in enumerate(predict):
    tot += 1
    if y == y_test[i]:
        n += 1

acc = n/tot * 100

print 'The preiction accuracy is {:.2f} %'.format(acc)
