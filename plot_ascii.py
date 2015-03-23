# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:06:18 2015

@author: Neill
"""

import glob
import os
import json
from matplotlib import pyplot as plt
import numpy as np

with open('config.json') as f:
    config = json.load(f)

path = os.path.join(config['datadir3'], '*.ASC')

for i, file_path in enumerate(glob.glob(path)):
    file_name = os.path.basename(file_path)
    file_name = file_name.replace('', '')[:-4]
    plot_path = config['datadir4']

    try:
        x, y = np.loadtxt(file_path, unpack=True)

    except ValueError:
        x, y, z = np.loadtxt(file_path, unpack=True)

    plt.figure(i)
    plt.plot(x, y)
    plt.xlabel("$2{\Theta}$")
    plt.ylabel('Counts')
    plt.title(file_name)
    plt.savefig(os.path.join(plot_path, '%s.pdf' % file_name), figsize=(5, 5),
                dpi=600)
    plt.close(i)
