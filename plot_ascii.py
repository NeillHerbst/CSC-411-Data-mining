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
import pandas as pd

# Get all working directories
with open('config.json') as f:
    config = json.load(f)

def filename(location, pattern):
    return os.path.expanduser(os.path.join(config[location], pattern))
    
def readpeaks(peakfile):
    # Load peak patterns
    d, I = np.loadtxt(peakfile, delimiter=',', skiprows=1, usecols=(4, 6),
                      unpack=True)
    # Calculate 2Theta values
    two_theta = 2 * np.arcsin(1.79/(2*d)) * 180/np.pi
    # Retrieve 3 largest peaks
    maxpeaks = heapq.nlargest(3, I)
    # Retrieve relative 2Theta values for Max peaks
    theta = []
    intens = []
    for i, val in enumerate(I):
        if val == maxpeaks[0] or val == maxpeaks[1] or \
          val == maxpeaks[2]:
            theta.append(two_theta[i])
            intens.append(val)
    return theta, intens

# Initialize the counter
n = 0

# Create path to datafiles
path = filename('ASCII Files', '*Sample*/*.ASC')

theta1, intens1 = readpeaks(filename('Peak Patterns', 'Hydrotalcite.csv'))
theta2, intens2 = readpeaks(filename('Peak Patterns', 'Hydrotalcite2.csv'))

plot_path = filename('Plot XRD', '')
excel_path = filename('Data', 'XRD_results.xlsx')
filename_lst = []

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
            # Save filename to excel spread sheet
            filename_lst.append(plot_name)

            # Counter
            n += 1

            # Load data from file
            x, y = np.loadtxt(file_path, usecols=(0, 1), unpack=True)

            # Get actual count values
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

# Saving excel file
excel_dict = {'Result': [np.NaN]*len(filename_lst), 'Sample No': filename_lst}
excel_df = pd.DataFrame(excel_dict)
excel_df.to_excel(excel_path)
