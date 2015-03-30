# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 23:01:20 2015

@author: Neill
"""

import os
import json
import PyPDF2 as pdf
import glob

# Getting all working directories
with open('config.json') as f:
    config = json.load(f)

# Create path to datafiles
path = os.path.join(config['datadir5'], 'XRD*.pdf')

# Create merger object
merger = pdf.PdfFileMerger()

# Cycling through all pdf files
for i, file_name in enumerate(glob.glob(path)):
    n = 1 + i
    merger.merge(open(file_name, 'rU'), i)

# Output file
merger.write(os.path.join(config['datadir5'], 'XRD Plots.pdf'))
