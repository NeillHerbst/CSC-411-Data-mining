import pandas as pd
import os
import json
import io


with open('config.json', 'rU') as f:
    config = json.load(f)

file_path = os.path.join(config['datadir2'], 'Sample 74 in air.txt')
txtfile = io.open(file_path, 'rU', encoding='iso8859')

details = {}
datapoints = []
read_names = []
names = ['']

# Collecting metadata
for line in txtfile:
    lineitems = line.strip().split('\t')

    if len(lineitems) == 2:
        details[lineitems[0]] = lineitems[1]
    else:
        details[lineitems[0]] = lineitems[1:]

    if "TGA Isothermal" in line:
        break

# Collecting header names
for i, line in enumerate(txtfile):

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

# Detecting line index of lines to be deleted
for i, line in enumerate(txtfile):
    if '2) TGA Temperature Scan' in line:
        del_line = i + 1
        break

# Reading data and populating DataFrame
txtfile.close()
txtfile = io.open(file_path, 'rU', encoding='iso8859')

for i, line in enumerate(txtfile):
    if 'Gas Flow' in line:
        break

datafile = pd.read_csv(txtfile, delimiter='\t', header=None)
dataframe = pd.DataFrame(datafile)
dataframe.columns = names

# Dropping unecessary lines and columns
for i, line in enumerate(txtfile):
    if '2) TGA Temperature Scan' in line:
        del_line = i
        break

dataframe = dataframe.drop('', axis=1)
dataframe = dataframe.drop(del_line, axis=0)
