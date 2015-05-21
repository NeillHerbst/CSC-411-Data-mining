# -*- coding: utf-8 -*-
"""
Created on Sun May 17 17:29:21 2015

@author: Neill
"""

from __future__ import division

import pandas as pd
import json
import os
import numpy as np
import re
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn import svm


# Retrieve all working directories
with open('config.json') as f:
    config = json.load(f)


def filename(location, pattern):
    return os.path.expanduser(os.path.join(config[location], pattern))


def data_filter(DataFrame, colums):
    df = DataFrame
    df = df[colums]
    for col in colums:
        if col != 'Elements / Ratio' and col != 'Item Name':
            df = df[np.isfinite(df[col])]
    df = df.reset_index(drop=True)

    return df


def component(DataFrame, column):
    df = DataFrame
    vals = df[column].fillna('')
    vals = vals.values
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

        elif line.strip() == '':
            ca_lst[i] = np.NaN
            mg_lst[i] = np.NaN

    return ca_lst, mg_lst


def result_finder(Sample_numbers, Results_file):
    results = filename('XRD Results', Results_file)
    results_file = pd.read_csv(results, sep=';')[['Result', 'Sample No']]
    XRD_results = results_file['Result']
    XRD_no = results_file['Sample No']
    matcher = re.compile(r'([0-9]+).([a-z]?)')
    matcher1 = re.compile('([0-9]+)([a-z]?)')
    results_lst = [np.NaN]*len(Sample_numbers)

    for i, s_num in enumerate(Sample_numbers):
        m1 = matcher1.match(s_num.strip())

        if m1:
            num1, subnum1 = m1.groups()
            if not subnum1:
                num1 = '{:04d}.a'.format(int(num1))

            elif subnum1:
                    num1 = '{:04d}.{}'.format(int(num1), subnum1)

            for j, xrd_num in enumerate(XRD_no):
                m2 = matcher.search(xrd_num.strip())

                if m2:
                    num2, subnum2 = m2.groups()
                    num2 = '{:04d}.{}'.format(int(num2), subnum2)

                    if num1 == num2:
                        results_lst[i] = XRD_results[j]
                    
    return results_lst


def plot(plt_data, results, data_name):
    plt.figure()
    target_names = ['No', 'Yes', 'Maybe', 'Partial']
#    target_names = ['No', 'Other']
    xj = 0.8

    if data_name == 'both Ca and Mg' or 'Mg':
        yj = 2.5*xj

    else:
        yj = xj

    for c, i, target_name in zip('rgyb', [0, 1, 2, 3], target_names):
        try:
            sns.regplot(plt_data[results == i, 0], plt_data[results == i, 1],
                        fit_reg=False, x_jitter=xj, y_jitter=yj,
                        label=target_name, color=c)

        except ValueError:
            pass

    plt.legend(bbox_to_anchor=(0., -0.15, 1., -0.1), loc=3,
               ncol=4, mode="expand", borderaxespad=0.)
    plt.title('Samples containing {}'.format(data_name))
    plt.xlabel('Stirrer time $(h)$')
    plt.ylabel(r'Temperature $\degree C$')
    plt.tight_layout()


def clf_Boundaries(X, Type, clf):
    h = 1
    # create a mesh to plot in
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                         np.arange(y_min, y_max, h))
    if Type == 'Ca':
        ca = np.ones(len(xx.ravel()))
        mg = np.zeros(len(xx.ravel()))

    elif Type == 'Mg':
        ca = np.zeros(len(xx.ravel()))
        mg = np.ones(len(xx.ravel()))

    elif Type == 'both':
        ca = np.ones(len(xx.ravel()))
        mg = np.ones(len(xx.ravel()))

    elif Type == 'None':
        ca = np.zeros(len(xx.ravel()))
        mg = np.zeros(len(xx.ravel()))

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel(), ca, mg])
    
    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)

    # Plot detail
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())


def plot_data_filter(Dataframe, Type, data_cols):
    df = Dataframe
    yes = [1]
    no = [0]

    if Type == 'Ca':
        data = df[df['Ca'].isin(yes)]
        data = data[data['Mg'].isin(no)]

    elif Type == 'Mg':
        data = df[df['Ca'].isin(no)]
        data = data[data['Mg'].isin(yes)]

    elif Type == 'both':
        data = df[df['Ca'].isin(yes)]
        data = data[data['Mg'].isin(yes)]

    elif Type == 'None':
        data = df[df['Ca'].isin(no)]
        data = data[data['Mg'].isin(no)]

    plot_data = data[data_cols].values
    results = data['Results'].values

    return plot_data, results

def save_plot(file_path, save=True, close=True):
    if save:
        plt.savefig(file_path)
    if close:
        plt.close()

# Data path
Dat_path = filename('Data', 'Sample_list_v3.0.xlsx')

# Data file
Dat_file = pd.ExcelFile(Dat_path).parse('Sample List')

# Dataframe
Df = pd.DataFrame(Dat_file)

# Colums used for SVM an PCA
collist = ['Item Name', 'Elements / Ratio', 'Stirrer Time', 'Temp (C)']

# Filtering data to remove rows containing empty values
Df = data_filter(Df, collist)

# Retrieving results for remaning files
results = result_finder(Df['Item Name'], 'XRD_Results.csv')

# Lists of results for samples containing Ca an Mg
ca_lst, mg_lst = component(Df, 'Elements / Ratio')

# Adding List of Ca, Mg and results to Dataframe
Df['Results'] = results
Df['Ca'] = ca_lst
Df['Mg'] = mg_lst

# Filtering samples that have no results file or Ca/Mg information
filter_lst = ['Stirrer Time', 'Temp (C)', 'Ca', 'Mg', 'Results']
Df = data_filter(Df, filter_lst)

# Fraction of data for training of SVM
frac = 1

# Calculating Dataframe split position
split = len(Df) * frac

# Data for SVM
x_lst = ['Stirrer Time', 'Temp (C)', 'Ca', 'Mg']
X = Df[x_lst]

x_train = X[X.index <= split]
x_test = X[X.index > split]

Y = Df.Results
#index = np.where(Y != 0)[0]
#Y[index] = 1
y_train = Y[Y.index <= split].values
y_test = Y[Y.index > split].values

# Creating SVM
clf = svm.SVC(kernel='linear',probability=True)
clf.fit(x_train, y_train)
#score = clf.score(x_test, y_test)

# Data colums used for plotting
data_cols = ['Stirrer Time', 'Temp (C)', 'Ca', 'Mg']

# Plotting All Data
plt_all = Df[data_cols].values
results_all = Df['Results'].values

# Plotting Samples Containing both Mg an Ca
plt_both, results_both = plot_data_filter(Df, 'both', data_cols)

# PLotting Samples containing only Ca
plt_ca, results_ca = plot_data_filter(Df, 'Ca', data_cols)

# Plotting Samples containing only Mg
plt_mg, results_mg = plot_data_filter(Df, 'Mg', data_cols)

# Plotting samples containing none
plt_no, results_no = plot_data_filter(Df, 'None', data_cols)

# File save format
fmt = 'pdf'

# File paths to save plots
plot_ca = filename('Plot XRD', 'Ca_Samples.{}'.format(fmt))
plot_mg = filename('Plot XRD', 'Mg_Samples.{}'.format(fmt))
plot_no = filename('Plot XRD', 'No_Mg_Ca_Samples.{}'.format(fmt))
plot_both = filename('Plot XRD', 'Both_Samples.{}'.format(fmt))
plot_all = filename('Plot XRD', 'All_Samples.{}'.format(fmt))

# Plotting all data
plot(plt_all, results_all, 'All data')
save_plot(plot_all, close=False)

# Plotting of Ca data
plot(plt_ca, results_ca, 'Ca')
clf_Boundaries(plt_ca, 'Ca', clf)
save_plot(plot_all, save=False, close=False)

# Plotting of Mg data
plot(plt_mg, results_mg, 'Mg')
clf_Boundaries(plt_mg, 'Mg', clf)
save_plot(plot_all)

# Plotting of Samples containing no Ca or Mg
plot(plt_no, results_no, 'no Mg or Ca')
clf_Boundaries(plt_no, 'None', clf)
save_plot(plot_all)

# Plotting of samples containing both Ca and Mg
plot(plt_both, results_both, 'both Ca and Mg')
clf_Boundaries(plt_both, 'both', clf)
save_plot(plot_all)
