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
import re

# Getting all working directories
with open('config.json') as f:
    config = json.load(f)

# Create path to datafiles
path = os.path.join(config['ASCII Files'], '*Sample*/*.ASC')

# Initializing the counter
n = 0

# Looping through all ASCII files
for i, file_path in enumerate(glob.glob(path)):

    # Reading individual file name and extracting sample number
    file_name = os.path.basename(file_path)
    file_name = file_name.replace('', '')[:-4]

    matcher = re.compile('.*[_ ]([0-9]+)([a-z]?).*')
    m = matcher.match(file_name)
    name_groups = m.groups()
    if name_groups[1] == '' or name_groups[1] == None:
        plot_name = 'XRD_' + str(name_groups[0]).zfill(4)
    else:
        plot_name = 'XRD_' + str(name_groups[0]).zfill(4) + '.' \
                    + str(name_groups[1])

    # Checking if plot allready exists
    exists = os.path.isfile(os.path.join(config['Plot XRD'],
                                         '{0}.pdf'.format(plot_name)))

    # Plotting non-existing files
    if exists is False:
            # Counter
        n += 1

        # Loading data form file
        x, y = np.loadtxt(file_path, usecols=(0, 1), unpack=True)

        # Plotting of ASCII files
        plot_path = config['Plot XRD']
        plt.figure(i)
        plt.plot(x, y)
        plt.xlabel("$2{\Theta}$")
        plt.ylabel('Counts')
        plt.title(file_name)
        plt.savefig(os.path.join(plot_path, '{0}.pdf'.format(plot_name)),
                    figsize=(5, 5), dpi=600)
        plt.close(i)
        
print '{0} Files plotted'.format(n)
