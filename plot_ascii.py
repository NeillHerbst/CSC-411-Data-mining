# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 20:06:18 2015

@author: Neill
"""

import os
import glob
import json
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import re
import heapq

# Getting all working directories
with open('config.json') as f:
    config = json.load(f)

# Create path to datafiles
path = os.path.join(config['ASCII Files'], '*Sample*/*.ASC')

# Create path to XRD peak patterns
XRD1 = os.path.join(config['Peak Patterns'], 'Hydrotalcite.csv')
XRD2 = os.path.join(config['Peak Patterns'], 'Hydrotalcite2.csv')

# Initializing the counter
n = 0

# Loading peak patterns
d1, I1 = np.loadtxt(XRD1, delimiter=',', skiprows=1, usecols=(4, 6),
                    unpack=True)
d2, I2 = np.loadtxt(XRD2, delimiter=',', skiprows=1, usecols=(4, 6),
                    unpack=True)
# Calculating 2Theta values
two_theta1 = 2 * np.arcsin(1.79/(2*d1)) * 180/np.pi
two_theta2 = 2 * np.arcsin(1.79/(2*d1)) * 180/np.pi

# Retrieving 3 largets peaks
maxpeaks1 = heapq.nlargest(3, I1)
maxpeaks2 = heapq.nlargest(3, I2)

# Retrieving relaive 2Theta values for Max peaks
theta1 = []
intens1 = []

theta2 = []
intens2 = []

for i, val in enumerate(I1):
    if val == maxpeaks1[0] or val == maxpeaks1[1] or \
     val == maxpeaks1[2]:
        theta1.append(two_theta1[i])
        intens1.append(val)

for i, val in enumerate(I2):
    if val == maxpeaks2[0] or val == maxpeaks2[1] or \
     val == maxpeaks2[2]:
        theta2.append(two_theta2[i])
        intens2.append(val)

    
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
        
        # getting actual count values
        peak1 = np.interp(theta1[0], x, y)
        peak2 = np.interp(theta2[0], x, y)
        plt_peak1 = []
        plt_peak2 = []

        for intens in intens1:
            plt_peak1.append(intens/100 * peak1)

        for intens in intens2:
            plt_peak2.append(intens/100 * peak2)

        # Plotting of ASCII files
        plot_path = config['Plot XRD']

        with PdfPages(os.path.join(plot_path, 'All plots.pdf')) as pdf:
            fig = plt.figure()
            plt.plot(x, y, 'k')

            for i in range(len(theta1)):
                plt.plot([theta1[i], theta1[i]], [0, plt_peak1[i]], 'r',
                         label='Hydrotalcite')

            for i in range(len(theta2)):
                plt.plot([theta2[i], theta2[i]], [0, plt_peak2[i]], 'b',
                         label='Hydrotalcite2')

            plt.xlabel("$2{\Theta}$")
            plt.ylabel('Counts')
            plt.title(plot_name)
            plt.legend(loc=0)
            plt.savefig(os.path.join(plot_path, '{0}.pdf'.format(plot_name)),
                        figsize=(5, 5), dpi=600)
            pdf.savefig()
            plt.close()
print '{0} Files plotted'.format(n)
