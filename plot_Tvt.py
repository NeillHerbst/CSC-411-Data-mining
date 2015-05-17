# -*- coding: utf-8 -*-
"""
Created on Sun May 17 17:29:21 2015

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
import time

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

# Timer
t0 = time.time()
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

Df = Df.sort_index(by=['Results', 'Ca', 'Mg'], ascending=[True, True, True])

yes = [1]
no = [0]
data_cols = ['Stirrer Time', 'Temp (C)']

# Samples Containing both Mg an Ca
both_data = Df[Df['Ca'].isin(yes)]
both_data = both_data[both_data['Mg'].isin(yes)]
plt_both = both_data[data_cols].values
results_both = both_data['Results'].values

# Samples containing only Ca
ca_data = Df[Df['Ca'].isin(yes)]
ca_data = ca_data[ca_data['Mg'].isin(no)]
plt_ca = ca_data[data_cols].values
results_ca = ca_data['Results'].values

# Samples containing only Mg
mg_data = Df[Df['Mg'].isin(yes)]
mg_data = mg_data[mg_data['Ca'].isin(no)]
plt_mg = mg_data[data_cols].values
results_mg = mg_data['Results'].values

# samples containing none
no_data = Df[Df['Ca'].isin(no)]
no_data = no_data[no_data['Mg'].isin(no)]
plt_no = no_data[data_cols].values
results_no = no_data['Results'].values


# Plotting
target_names = ['No', 'Yes', 'Maybe', 'Partial']
plot_ca = filename('Plot XRD', 'Ca_Samples.pdf')
plot_mg = filename('Plot XRD', 'Mg_Samples.pdf')
plot_no = filename('Plot XRD', 'No_Mg_Ca_Samples.pdf')
plot_both = filename('Plot XRD', 'Both_Samples.pdf')

# Plotting of Ca data
plt.figure(figsize = (10, 6))
for c, i, target_name in zip("rgym", [0, 1, 2, 4], target_names):
    plt.scatter(plt_ca[results_ca == i, 0], plt_ca[results_ca == i, 1],
                c=c, label=target_name)
plt.legend(bbox_to_anchor=(0., -0.15, 1., -0.1), loc=3,
           ncol=4, mode="expand", borderaxespad=0.)
plt.title('Samples containing Ca')
plt.xlabel('Stirrer time $(h)$')
plt.ylabel(r'Temperature $\degree C$')
plt.xlim(xmin=-5)
plt.savefig(plot_ca)
plt.close()


# Plotting of Mg data
plt.figure(figsize = (10, 6))
for c, i, target_name in zip("rgym", [0, 1, 2, 4], target_names):
    plt.scatter(plt_mg[results_mg == i, 0], plt_mg[results_mg == i, 1],
                c=c, label=target_name)
plt.legend(bbox_to_anchor=(0., -0.15, 1., -0.1), loc=3,
           ncol=4, mode="expand", borderaxespad=0.)
plt.title('Samples containing Mg')
plt.xlim(xmin=-5)
plt.xlabel('Stirrer time $(h)$')
plt.ylabel(r'Temperature $\degree C$')
plt.savefig(plot_mg)
plt.close()

# Plotting of Samples containing no Ca or Mg
plt.figure(figsize = (10, 6))
for c, i, target_name in zip("rgym", [0, 1, 2, 4], target_names):
    plt.scatter(plt_no[results_no == i, 0], plt_no[results_no == i, 1],
                c=c, label=target_name)
plt.legend(bbox_to_anchor=(0., -0.15, 1., -0.1), loc=3,
           ncol=4, mode="expand", borderaxespad=0.)
plt.title('Samples containing no Ca or Mg')
plt.xlim(xmin=-5)
plt.xlabel('Stirrer time $(h)$')
plt.ylabel(r'Temperature $\degree C$')
plt.savefig(plot_no)
plt.close()

# Plotting of samples containing both Ca and Mg
plt.figure(figsize = (10, 6))
for c, i, target_name in zip("rgym", [0, 1, 2, 4], target_names):
    plt.scatter(plt_both[results_both == i, 0], plt_both[results_both == i, 1], 
                c=c, label=target_name)
plt.legend(bbox_to_anchor=(0., -0.15, 1., -0.1), loc=3,
           ncol=4, mode="expand", borderaxespad=0.)
plt.title('Samples containing both Ca and Mg')
plt.xlim(xmin=-5)
plt.xlabel('Stirrer time $(h)$')
plt.ylabel(r'Temperature $\degree C$')
plt.savefig(plot_both)
plt.close()
