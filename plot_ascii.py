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

TWOTHETA_CUTOFF = 5
METHOD = 'all'

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
    theta, intens = zip(*[(twot, val) for twot, val in zip(two_theta, I)
                          if val in maxpeaks[:3]])
    return name, theta, intens


def method_filter(method):

    # Retrieving files
    xl_file_path = filename('Data', 'Sample_list_database.xlsx')
    xl_file_main = pd.ExcelFile(xl_file_path)
    xl_batches = xl_file_main.parse('Batches')
    xl_syn_names = xl_file_main.parse('Synthesis')

    # creating arrays
    batch_id = xl_batches['batch_id'][:].values
    syn_id = xl_batches['syn_id'][:].values
    syn_names = xl_syn_names['description'][:].values
    syn_names_id = xl_syn_names['syn_id'][:].values

    if method == 'all':
        return batch_id, syn_id, syn_names, syn_names_id

    elif method != 'all':
        # retrieving method id as displayed in excel file
        m_id = np.where(syn_names == method)[0][0] + 1

        # filtering values
        batch_index = np.where(syn_id != m_id)
        batch_id = np.delete(batch_id, batch_index)
        syn_id = np.delete(syn_id, batch_index)

        return batch_id, syn_id, syn_names, syn_names_id


def method_name(batch_id, batch_file, METHOD):
    if batch_file in batch_id:
        method_found = True
        if METHOD == 'all':
            syn_index = np.where(batch_id == batch_file)[0][0]
            syn_id = syn_ids[syn_index]

            if np.isfinite(syn_id):
                name_id = np.where(syn_names_id == syn_id)[0][0]
                syn_name = syn_names[name_id]

            else:
                method_found = False
                syn_name = None
        else:
            syn_name = METHOD
    else:
            method_found = False
            syn_name = None

    return syn_name, method_found

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
output_path = filename('Data', 'XRD_results.csv')
filename_lst = []

# filtering methods from sample list
batch_id, syn_ids, syn_names, syn_names_id = method_filter(METHOD)
k = 0
matcher = re.compile('.*[_ ]([0-9]+)([a-z]?).*')
# Loop through all ASCII files
with PdfPages(os.path.join(plot_path, 'All plots.pdf')) as pdf:
    for i, file_path in enumerate(glob.glob(path)):
        # Read individual file name and extracting sample number
        file_name = os.path.basename(file_path)
        file_name = file_name.replace('', '')[:-4]

        m = matcher.match(file_name)
        number, subnumber = m.groups()

        # batch number from XRD file name
        batch_file = str(number).zfill(3) + subnumber

        # Comparing XRD file number with sample list number and retrieving method name
        syn_name, method_found = method_name(batch_id, batch_file, METHOD)
        
#        if not subnumber:
#            subnumber = 'a'
#        plot_name = 'XRD_{0:04d}.{1}'.format(int(number), subnumber)
#
#        # Check if plot already exists
#        plot_filename = os.path.join(plot_path, '{0}.pdf'.format(plot_name))
#        exists = os.path.isfile(plot_filename)
#
#        # Plot non-existing files
#        if exists:
#            # Save filename to record
#            filename_lst.append(plot_name)
#
#            # Counter
#            n += 1
#
#            # Load data from file
#            x, y = np.loadtxt(file_path, usecols=(0, 1), unpack=True)
#
#            # Filter for 2theta cutoff
#            good = x >= TWOTHETA_CUTOFF
#            x = x[good]
#            y = y[good]
#
#            # Plot data
#            fig = plt.figure()
#            plt.plot(x, y, 'k')
#
#            # Plot peaks
#            for linefmt, (name, theta, intens) in zip(linefmts, peakpatterns):
#                # Get actual count values
#                peak = np.interp(theta[0], x, y)
#                plt_peak = np.array(intens)/100.*peak
#                plt.stem(theta, plt_peak,
#                         linefmt=linefmt, markerfmt=' ', basefmt=' ',
#                         label=name)
#
#            plt.xlabel(r"$2\theta$")
#            plt.ylabel('Counts')
#            plt.title(plot_name)
#            plt.legend(loc=0)
#
#            if method_found:
#                plt.figtext(0.73, 0.68, syn_name, weight='bold')
#
##            plt.savefig(plot_filename)
##            pdf.savefig()
#            plt.close()
#print '{0} Files plotted'.format(n)

# Save file
#output_dict = {'Result': [np.NaN]*len(filename_lst), 'Sample No': filename_lst}
#output_df = pd.DataFrame(output_dict)
#output_df.to_csv(output_path)
