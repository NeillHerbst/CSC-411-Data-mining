# -*- coding: utf-8 -*-
"""
Created on Wed May 13 13:12:24 2015

@author: Neill
"""

from sklearn import svm
import pandas as pd
import json
import os
import numpy as np

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
collist = ['Stirrer Time', 'Temp (C)', 'Result']

# Adjusting Dataframe to only include important colums
Df = Df[collist]

# Filtering dataframe to remove rows with no values
Df = Df[np.isfinite(Df.Result)]
Df = Df[np.isfinite(Df['Temp (C)'])]
Df = Df[np.isfinite(Df['Stirrer Time'])]

