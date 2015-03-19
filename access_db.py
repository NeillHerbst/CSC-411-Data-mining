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
path2 = os.path.join(config['datadir'], 'access.db')

try:
    con1 = lite.connect(':memory: access.db')
    con2 = lite.connect(path2)
    datafile = pd.ExcelFile(path1)
    stop = False

except IOError:
    print 'One of the files does not exist'
    stop = True

if stop is False:
    with con1:
        cur = con1.cursor()
        people = datafile.parse('People', header=0)
        batches = datafile.parse('Batches', header=0)
        synthesis = datafile.parse('Synthesis', header=0)
        parm_type = datafile.parse('Parm type', header=0)
        parameters = datafile.parse('Parameters', header=0)
        values = datafile.parse('Parm values', header=0)

        people_df = pd.DataFrame(people)
        batches_df = pd.DataFrame(batches)
        synthesis_df = pd.DataFrame(synthesis)
        parm_type_df = pd.DataFrame(parm_type)
        parameters_df = pd.DataFrame(parameters)
        values_df = pd.DataFrame(values)

        people_df.to_sql('People', con1, if_exists='replace')
        batches_df.to_sql('Batches', con1, if_exists='replace')
        synthesis_df.to_sql('Synthesis', con1, if_exists='replace')
        parm_type_df.to_sql('Parm_type', con1, if_exists='replace')
        parameters_df.to_sql('Parameters', con1, if_exists='replace')
        values_df.to_sql('Parm_values', con1, if_exists='replace')

    with con2 and con1:
        cur1 = con1.cursor()
        cur2 = con2.cursor()
        cur2.executescript('''
        drop table if exists Parm_values;
        drop table if exists People;
        drop table if exists Batches;
        drop table if exists Synthesis;
        drop table if exists Parm_type;
        drop table if exists Parameters;
        drop table if exists Parameter;
        drop table if exists Par_values;

        create table Parm_values(batch_id INT, syn_id INT, step_id INT, par_id INT, val);
        create table People(owner_id INT PRIMARY KEY, description TEXT);
        create table Batches(batch_id TEXT PRIMARY KEY, syn_id INT, owner_id);
        create table Synthesis(syn_id INT PRIMARY KEY, description TEXT);
        create table Parm_type(type_id INT PRIMARY KEY, type TEXT);
        create table Parameters(par_id INT PRIMARY KEY, type_id INT, description TEXT);
        ''')

        table1 = cur1.execute('select owner_id, description from People')
        data1 = cur1.fetchall()
        print data1[0][0]
        cur2.execute('insert into People values (?,?) ', [data1[0][0], data1[0][1]])
        con2.commit()