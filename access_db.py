# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 14:28:40 2015

@author: Neill
"""

import sqlite3 as lite
import pandas as pd
import json
import os

with open('config.json') as f:
    config = json.load(f)

path1 = os.path.join(config['datadir'], 'Sample_list_norm2.xlsx')
path2 = os.path.join(config['datadir1'], 'access.db')

try:
    con = lite.connect(path2)
    datafile = pd.ExcelFile(path1)
    stop = False

except IOError:
    print 'One of the files does not exist'
    stop = True

if stop is None:
    with con:
        cur = con.cursor()
        people = datafile.parse('People', header=0)
        batches = datafile.parse('Batches', header=0)
        synthesis = datafile.parse('Synthesis', header=0)
        parm_type = datafile.parse('Parm type', header=0)
        parameters = datafile.parse('Parameters', header=0)
        values = datafile.parse('Parm values', header=0)

        people_df = pd.DataFrame(people)
        batches_df = pd.DataFrame(people)
        synthesis_df = pd.DataFrame(people)
        parm_type_df = pd.DataFrame(people)
        parameters_df = pd.DataFrame(people)
        values_df = pd.DataFrame(people)

        people_df.to_sql('People', con, if_exists='replace')
        batches_df.to_sql('Batches', con, if_exists='replace')
        synthesis_df.to_sql('Synthesis', con, if_exists='replace')
        parm_type_df.to_sql('Parm type', con, if_exists='replace')
        parameters_df.to_sql('Parameter', con, if_exists='replace')
        values_df.to_sql('Parm values', con, if_exists='replace')

    con.close()
