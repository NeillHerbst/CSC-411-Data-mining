import pandas as pd
import os
import json
import io


with open('config.json', 'rU') as f:
    config = json.load(f)

txtfile = os.path.join(config['datadir2'], 'Sample 74 in air.txt')
datafile = io.open(txtfile, 'rU', encoding='iso8859')

details = {}
datapoints = []
read_names = []
names = ['']

# Collecting metadata
for line in datafile:
    lineitems = line.strip().split('\t')

    if len(lineitems) == 2:
        details[lineitems[0]] = lineitems[1]
    else:
        details[lineitems[0]] = lineitems[1:]

    if "TGA Isothermal" in line:
        break

# Collecting header names
for i, line in enumerate(datafile):

    if 'Time' in line:
        lineitems = line.strip().split('\t')
        for i in range(len(lineitems)):
            read_names.append(lineitems[i])

    if 'Gas Flow' in line:
        lineitems = line.strip().split('\t')
        for i in range(len(lineitems)):
            read_names.append(lineitems[i])

    if '0.000000' in line:
        break

for i in range(7):
    if i == 0:
        names.append(read_names[0].rstrip())
    else:
        names.append(read_names[i].rstrip() + ' ' + read_names[i + 6].rstrip())

# Reading data and populating DataFrame
datafile.close()
datafile = io.open(txtfile, 'rU', encoding='iso8859')

for i, line in enumerate(datafile):
    if 'Gas Flow' in line:
        break

datafile = pd.read_csv(datafile, delimiter='\t', header=None)
dataframe = pd.DataFrame(datafile)
dataframe.columns = names
