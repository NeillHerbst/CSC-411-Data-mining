import sqlite3 as lite
import pandas as pd
import json
import os


with open('config.json') as f:
    config = json.load(f)

path1 = os.path.join(config['datadir'],'Sample_list.xlsx')
path2 = os.path.join(config['datadir1'],'Data_mining.db')
    
try:
    con = lite.connect(path2)
    datafile = pd.ExcelFile(path1)
    stop = None
    
except IOError:
    print 'One of the files does not exist'
    stop = 'yes'

if stop == None:
    with con:
        cur = con.cursor()
        datafile = datafile.parse('Sample List',header=1,skiprows=0)
        dataframe  = pd.DataFrame(datafile)
        
        headers = ['Delt','Serial', 'Item_Name', 'Vendor_Name','Catalog','Owner','Top_Loc',\
                    'Sub_Loc', 'Loc_Details', 'Price', 'Unit_Size', 'Expr',\
                    'Quant', 'CAS', 'Created_By', 'Details', 'URL', \
                    'Byproduct', 'Elements/Ratio','HTC_Formed', 'Lab_Book',\
                    'Msizer','Method', 'pH', 'Pres', 'Stir_Time', 'Temp',\
                    'TGA','XRD']
                    
        dataframe.columns = headers
        dataframe.to_sql('Sample_list',con, if_exists='replace')
        
    con.close()
