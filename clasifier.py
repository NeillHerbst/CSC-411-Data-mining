# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:12:24 2015

@author: Neill
"""

from sklearn import svm
import pandas as pd
import json
import os
import numpy

# Get all working directories
with open('config.json') as f:
    config = json.load(f)


def filename(location, pattern):
    return os.path.expanduser(os.path.join(config[location], pattern))

# Data path
Dat_path = filename('Data', 'Sample_list_v2.0.xlsx')

# Data file
Dat_file = pd.ExcelFile(Dat_path)
Dat_file = Dat_file.parse('Sample List')

# Dataframe
Df = pd.DataFrame(Dat_file)

# Important colums
collist = ['Elements / Ratio','Stirrer Time', 'Temp (C)']

# Adjusting Dataframe to only inclue important colums
Df = Df[collist]

print Df