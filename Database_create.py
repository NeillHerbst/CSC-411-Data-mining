import sqlite3
import os
import json

with open('config.json') as f:
    config = json.load(f)

path = os.path.join(config['datadir1'],'Data_mining.db')

try:
    con = lite.connect(path)

except IOError,e:
    print e
    
con.close()
