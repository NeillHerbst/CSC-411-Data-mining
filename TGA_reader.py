import pandas as pd
import os
import json

with open('config.json') as f:
    config = json.load(f)

txtfile = os.path.join(config['datadir2'],'Sample 74 in air.txt')
details ={}
datafile = open(txtfile,'rU')

for line in datafile:
    if "0.000000" in line:
        break
    lineitems = line.strip().split('\t')
    
    if len(lineitems)==2:
        details[lineitems[0]] = lineitems[1]
    else:
            details[lineitems[0]] = lineitems[1:]
            
names = ['Experiment','Time', 'Unsub_weight', 'Base_weight','Prog_Temp','Samp_Temp','G_Flow','Diag_Temp']


datafile = pd.read_csv(txtfile,delimiter='\t',skiprows=33)
dataframe = pd.DataFrame(datafile)
dataframe.columns = names
