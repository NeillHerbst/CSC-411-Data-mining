import sqlite3 as lite
import os
import json

with open('config.json') as f:
    config = json.load(f)

path = os.path.join(config['Data'], 'access.db')

try:
    con = lite.connect(path)

except IOError, e:
    print e

con.close()
