import sqlite3 as lite
import pandas as pd

# Change file paths to where database and data files are stored
con = lite.connect('/Users/Neill/Dropbox/CSC411 Data Mining (N Herbst)/data/Data_mining.db')

with con:
    cur = con.cursor()
    datafile = pd.ExcelFile('/Users/Neill/Dropbox/CSC411 Data Mining (N Herbst)/data/Sample_list.xlsx')
    datafile = datafile.parse('Sample List',header=1,skiprows=0)
    dataframe  = pd.DataFrame(datafile)
    dataframe.to_sql('Sample_list',con, if_exists='replace')
    
con.close()
