import csv
import sqlite3 as lite

con = lite.connect('Data_mining.db')
cur = con.cursor()
cur.execute('drop table if exists sample_list')
cur.execute('drop table if exists csv')
cur.execute('create table sample_list (col1, col2, col3, col4, col5, col6, col7, col8, col9, col10,\
                                col11, col12, col13, col14, col15, col16, col17, col18, col19,\
                                col20, col21, col22, coll23, col24, col25, col26, col27, col28,\
                                col29);')

with open('Sample_list.csv','rU') as fin:
    dr = csv.DictReader(fin, delimiter=';',dialect='excel')
    to_db = [(i['Delete? (Y/N)'], i['Serial#'], i['Item Name'], i['Vendor Name'],\
            i['Catalog No'], i['Owner'], i['Top Location'], i['Sub Location'],\
            i['Location Details'], i['Price'], i['Unit Size'], i['Expiration Date(mm/dd/yyyy)'],\
            i['Quantity'], i['CAS Number'], i['Created By'], i['Technical Details'],\
            i['URL'], i['Byproduct Formed (Species)'], i['Elements / Ratio'],\
            i['HTC Formed (Counts)'], i['Lab Book'], i['Mastersizer'],i ['Method'],\
            i['pH'], i['Pressure (kPa)'], i['Stirrer Time'], i['Temp (C)'], i['TGA'],\
            i['XRD'])for i in dr]
    
cur.executemany("insert into sample_list (col1, col2, col3, col4, col5, col6, col7, col8, col9,\
                                col10, col11, col12, col13, col14, col15, col16, col17,\
                                col18, col19, col20, col21, col22, coll23, col24, col25,\
                                col26, col27, col28, col29) \
                                Values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
                                        ?,?,?,?,?,?,?,?,?)",to_db)
con.commit()
con.close()
