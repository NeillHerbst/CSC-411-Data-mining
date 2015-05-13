# -*- coding: utf-8 -*-
"""
Created on Wed May 13 19:38:32 2015

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
    
# Results path
results = filename('XRD Results', 'XRD_Results.csv')
Dat_path = filename('Data', 'Sample_list_v2.0.xlsx')

Data = pd.ExcelFile(Dat_path).parse('Sample List')
sample_lst_no = pd.DataFrame(Data)[r'Item Name']
results_file = pd.read_csv(results, sep=';')[['Result', 'Sample No']]
XRD_results = results_file['Result']
XRD_no = results_file['Sample No']


matcher = re.compile(r'([0-9]+)[.]([a-z]?)')
matcher1 = re.compile('([0-9]+)([a-z]?)')

results_init = np.zeros(len(sample_lst_no))

for i, s_num in enumerate(sample_lst_no):

    m1 = matcher1.match(s_num)
    if m1:
        num1, subnum1 =  m1.groups()
        if not subnum1:
            num1 = '{:04d}.a'.format(int(num1))
        
        elif subnum1:
                num1 = '{:04d}.{}'.format(int(num1), subnum1)
#        print num1   
        for j, xrd_num in enumerate(XRD_no):
#            print s_num, xrd_num
            m2 = matcher.match(xrd_num)
            print m2, xrd_num
            if m2:
                num2, subnum2 = m2.groups()
                num2 = '{}.{}'.format(int(num2), subnum2)
                print num2
                if num1 == num2:
                    results_init[i] = XRD_results[j]
