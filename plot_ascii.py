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
    name = os.path.basename(peakfile)[:-4]
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
    return name, theta, intens

# Initialize the counter
n = 0

# Create path to datafiles
path = filename('ASCII Files', '*Sample*/*.ASC')

peakpatterns = [readpeaks(peakfile)
                for peakfile in glob.glob(filename('Peak Patterns', '*.csv'))]
# 5 point qualitative scale from http://colorbrewer2.org/
# TODO: Use seaborn (http://stanford.edu/~mwaskom/software/seaborn/) instead
linefmts = ['#1b9e77', '#d95f02', '#7570b3', '#e7298a', '#66a61e']

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

            # Plot data
            fig = plt.figure()
            plt.plot(x, y, 'k')

            # Plot peaks
            for linefmt, (name, theta, intens) in zip(linefmts, peakpatterns):
                # Get actual count values
                peak = np.interp(theta[0], x, y)
                plt_peak = np.array(intens)/100.*peak
                plt.stem(theta, plt_peak,
                         linefmt=linefmt, markerfmt=' ', basefmt=' ',
                         label=name)

            plt.xlabel(r"$2\theta$")
            plt.ylabel('Counts')
            plt.title(plot_name)
            plt.legend(loc=0)
            plt.savefig(plot_filename)
            pdf.savefig()
            plt.close()
print '{0} Files plotted'.format(n)

# Save Excel file
excel_dict = {'Result': [np.NaN]*len(filename_lst), 'Sample No': filename_lst}
excel_df = pd.DataFrame(excel_dict)
excel_df.to_excel(excel_path)
