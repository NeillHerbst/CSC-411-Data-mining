import sqlite3 as lite
import pandas as pd

# Change file paths to where database and data files are stored
con = lite.connect('/Users/Neill/Dropbox/CSC411 Data Mining (N Herbst)/data/Data_mining.db')

with con:
    cur = con.cursor()
    datafile = pd.ExcelFile('/Users/Neill/Dropbox/CSC411 Data Mining (N Herbst)/data/Sample_list.xlsx')
    datafile = datafile.parse('Sample List',header=1,skiprows=0)
    dataframe  = pd.DataFrame(datafile)
    
    headers = ['Delete?','Serial_No', 'Item_Name', 'Vendor_Name','Catalog_No','Owner','Top_Location',\
                'Sub_Location', 'Location_Details', 'Price', 'Unit_Size', 'Expiration_Date(mm/dd/yyyy)',\
                'Quantity', 'CAS_Number', 'Created_By', 'Technical_Details', 'URL', \
                'Byproduct_Formed_(Species)', 'Elements/Ratio','HTC_Formed_(Counts)', 'Lab_Book',\
                'Mastersizer','Method', 'pH', 'Pressure_(kPa)', 'Stirrer_Time', 'Temp_(C)',\
                'TGA','XRD']
                
    dataframe.columns = headers
    dataframe.to_sql('Sample_list',con, if_exists='replace')
    
con.close()
