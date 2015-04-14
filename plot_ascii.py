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

# Get all working directories
with open('config.json') as f:
    config = json.load(f)

def filename(location, pattern):
    return os.path.expanduser(os.path.join(config[location], pattern))
    
# Create path to datafiles
path = filename('ASCII Files', '*Sample*/*.ASC')

# Create path to XRD peak patterns
XRD1 = filename('Peak Patterns', 'Hydrotalcite.csv')
XRD2 = filename('Peak Patterns', 'Hydrotalcite2.csv')

# Initialize the counter
n = 0

# Load peak patterns
d1, I1 = np.loadtxt(XRD1, delimiter=',', skiprows=1, usecols=(4, 6),
                    unpack=True)
d2, I2 = np.loadtxt(XRD2, delimiter=',', skiprows=1, usecols=(4, 6),
                    unpack=True)
# Calculate 2Theta values
two_theta1 = 2 * np.arcsin(1.79/(2*d1)) * 180/np.pi
two_theta2 = 2 * np.arcsin(1.79/(2*d1)) * 180/np.pi

# Retrieve 3 largets peaks
maxpeaks1 = heapq.nlargest(3, I1)
maxpeaks2 = heapq.nlargest(3, I2)

# Retrieve relative 2Theta values for Max peaks
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

plot_path = filename('Plot XRD', '')

# Loop through all ASCII files
with PdfPages(os.path.join(plot_path, 'All plots.pdf')) as pdf:
    for i, file_path in enumerate(glob.glob(path)):

        # Read individual file name and extracting sample number
        file_name = os.path.basename(file_path)
        file_name = file_name.replace('', '')[:-4]

        matcher = re.compile('.*[_ ]([0-9]+)([a-z]?).*')
        m = matcher.match(file_name)

        number, subnumber = m.groups()
        if not subnumber:
            subnumber = 'a'
        plot_name = 'XRD_{0:04d}.{1}'.format(int(number), subnumber)

        # Check if plot already exists
        plot_filename = os.path.join(plot_path, '{0}.pdf'.format(plot_name))
        exists = os.path.isfile(plot_filename)

        # Plot non-existing files
        if not exists:
                # Counter
            n += 1

            # Load data from file
            x, y = np.loadtxt(file_path, usecols=(0, 1), unpack=True)

            # get actual count values
            peak1 = np.interp(theta1[0], x, y)
            peak2 = np.interp(theta2[0], x, y)
            plt_peak1 = []
            plt_peak2 = []

            for intens in intens1:
                plt_peak1.append(intens/100 * peak1)

            for intens in intens2:
                plt_peak2.append(intens/100 * peak2)

            # Plot ASCII files
            fig = plt.figure()
            plt.plot(x, y, 'k')

            plt.stem(theta1, plt_peak1,
                     linefmt='r', markerfmt=' ', basefmt=' ',
                     label='Hydrotalcite')

            plt.stem(theta2, plt_peak2,
                     linefmt='b', markerfmt=' ', basefmt=' ',
                     label='Hydrotalcite2')

            plt.xlabel("$2\theta$")
            plt.ylabel('Counts')
            plt.title(plot_name)
            plt.legend(loc=0)
            plt.savefig(plot_filename,
                        figsize=(5, 5), dpi=600)
            pdf.savefig()
            plt.close()
print '{0} Files plotted'.format(n)
