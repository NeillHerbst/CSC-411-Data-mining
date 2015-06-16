import sqlite3 as lite
import pandas as pd
import json
import os
import numpy as np


with open('config.json') as f:
    config = json.load(f)

path1 = os.path.join(config['Data'], 'Sample_list.xlsx')
path2 = os.path.join(config['Data'], 'Data_mining.db')

con = lite.connect(path2)

# Test if datafile exists
data = os.path.isfile(path1)
if data:
    datafile = pd.ExcelFile(path1)
    stop = None

else:
    stop = True
    filename = os.path.basename(path1)
    direc = os.path.dirname(path1)
    print '"{}" does not exist in the directory: "{}"'.format(filename, direc)


if not stop:
    with con:
        cur = con.cursor()
        datafile = datafile.parse('Sample List', header=1, skiprows=0)
        dataframe  = pd.DataFrame(datafile)

        headers = ['Delt', 'Serial', 'Item_Name', 'Vendor_Name', 'Catalog', 'Owner',
                   'Top_Loc','Sub_Loc', 'Loc_Details', 'Price', 'Unit_Size', 'Expr',
                    'Quant', 'CAS', 'Created_By', 'Details', 'URL',
                    'Byproduct', 'Elements/Ratio', 'HTC_Formed', 'Lab_Book',
                    'Msizer', 'Method', 'pH', 'Pres', 'Stir_Time', 'Temp',
                    'TGA', 'XRD']

        dataframe.columns = headers
        dataframe.to_sql('Sample_list', con, if_exists='replace')

    con.close()
