# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:06:18 2015

@author: Neill
"""


import os
import glob
import json
from matplotlib import pyplot as plt
import numpy as np

# Getting all working directories
with open('config.json') as f:
    config = json.load(f)

# Create path to datafiles
path = os.path.join(config['datadir4'], '*/*.ASC')

# Initializing the counter
n = 0

# Looping through all ASCII files
for i, file_path in enumerate(glob.glob(path)):

    # Reading individual file name and extracting sample number
    file_name = os.path.basename(file_path)
    file_name = file_name.replace('', '')[:-4]

    sample = file_name.split('_')
    if len(sample) == 2:
        name2 = sample[-1].split(' ')
        if len(name2) == 1:
            sample_no = sample[-1]
        elif len(name2) == 2:
            sample_no = name2[-1]

    elif len(sample) == 3:
        sample_no = sample[1]

    elif len(sample) == 1:
        sample = file_name.split(' ')
        sample_no = sample[-1]

    # Counter
    n += 1

    # Loading data form file
    x, y = np.loadtxt(file_path, usecols=(0, 1), unpack=True)

    # Plotting of ASCII files
    plot_path = config['datadir5']
    plt.figure(i)
    plt.plot(x, y)
    plt.xlabel("$2{\Theta}$")
    plt.ylabel('Counts')
    plt.title(file_name)
    plt.savefig(os.path.join(plot_path, 'XRD_%s.pdf' % sample_no),
                figsize=(5, 5), dpi=600)
    plt.close(i)

print '%s Files plotted' % n
