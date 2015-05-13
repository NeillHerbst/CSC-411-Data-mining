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
import re

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

    matcher = re.compile(r"(Ca\b|Ca\d|Ca[^O,o]|Cal[M,m]|Calcium|Lime|Katoite|\
                         kat|[H, h]ydrocalumite|[P, p]ortlanite|[D,d]olomite)\
                         |(Mg\b|Mg\d|\Mg[^O,o]|Mag\b|Magnesium|Bricite\
                         |[M, m]eixnerite|HTC|[H, h]ydrotalcite|Dolomite\
                         |Pyrosorb|Alcimazer|Meix)|([C, c]alcined)")

    for i, line in enumerate(vals):
        m = matcher.match(line.strip())
        if m:
            ca, mg, calcined = m.groups()
            if ca and not calcined:
                ca_lst[i] = 1

            if mg:
                mg_lst[i] = 1

    return ca_lst, mg_lst

# Data path
Dat_path = filename('Data', 'Sample_list_v2.0.xlsx')

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

# Fraction of data for training
frac = 0.8

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
