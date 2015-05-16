# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:12:24 2015

@author: Neill
"""
from __future__ import division
from sklearn import svm
from sklearn import decomposition as decomp
import pandas as pd
import json
import os
import numpy as np
import re
from matplotlib import pyplot as plt

# Retrieve all working directories
with open('config.json') as f:
    config = json.load(f)


def filename(location, pattern):
    return os.path.expanduser(os.path.join(config[location], pattern))


def data_filter(DataFrame, colums):
    df = DataFrame
    df = df[collist]
    for col in colums:
        if col != 'Elements / Ratio':
            df = df[np.isfinite(df[col])]
    df = df.reset_index(drop=True)
    return df


def component(DataFrame, column):
    df = DataFrame
    vals = df[column].values
    Npoints = len(vals)
    ca_lst = np.zeros(Npoints)
    mg_lst = np.zeros(Npoints)

    ca_matcher = re.compile('(Ca\\b|Ca\\d|Ca[^O,o,r,l,t]|CalMag|Calcium|Lime\
                             |Katoite|kat|Hydrocalumite|Portlanite|\
                             Dolomite)', re.IGNORECASE)

    mg_matcher = re.compile('(Mg|Mg\\b|Mg\\d|Mg[^O,o]|CalMag|Magnesium\
                             |Bricite|Meixnerite|HTC|Hydrotalcite|\
                             Dolomite|Pyrosorb|Alcimazer|Meix)', re.IGNORECASE)

    for i, line in enumerate(vals):
        m_ca = ca_matcher.search(line.strip())
        m_mg = mg_matcher.search(line.strip())

        if m_ca and m_mg:
            ca_lst[i] = 1
            mg_lst[i] = 1

        elif m_ca or m_mg:
            if m_ca:
                ca_lst[i] = 1

            if m_mg:
                mg_lst[i] = 1

    return ca_lst, mg_lst

# Data path
Dat_path = filename('Data', 'Sample_list_v3.0.xlsx')

# Data file
Dat_file = pd.ExcelFile(Dat_path).parse('Sample List')

# Dataframe
Df = pd.DataFrame(Dat_file)

# Colums used for SVM
collist = ['Elements / Ratio', 'Stirrer Time', 'Temp (C)', 'Result']

# Filtering data to remove rows containing empty values
Df = data_filter(Df, collist)

# Lists of results for samples containing Ca an Mg
ca_lst, mg_lst = component(Df, 'Elements / Ratio')

# Adding List of Ca and Mg results to Dataframe
Df['Ca'] = ca_lst
Df['Mg'] = mg_lst

# Columns for PCA
pca_cols = ['Stirrer Time', 'Temp (C)', 'Ca', 'Mg']

# Data Decomp
pca = decomp.PCA(whiten=True)
X = Df[pca_cols]
trans = pca.fit_transform(X)

# Fraction of data for training
frac = 0.5

# Calculating Dataframe split position
split = len(Df) * frac

# Data for SVM
x_lst = ['Stirrer Time', 'Temp (C)', 'Ca', 'Mg']
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

print 'The prediction accuracy is {:.2f} %'.format(acc)
