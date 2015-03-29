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

path1 = os.path.join(config['datadir'], 'Sample_list_database.xlsx')
path2 = os.path.join(config['datadir'], 'access.db')

try:
    con = lite.connect(path2)
    datafile = pd.ExcelFile(path1)
    stop = False

except IOError:
    print 'One of the files does not exist'
    stop = True

if stop is False:
    with con:
        cur = con.cursor()
        people = datafile.parse('People', header=0)
        batches = datafile.parse('Batches', header=0)
        synthesis = datafile.parse('Synthesis', header=0)
        parm_type = datafile.parse('Parm type', header=0)
        parameters = datafile.parse('Parameters', header=0)
        values = datafile.parse('Parm values', header=0)
        steps = datafile.parse('Steps', header=0)

        people_df = pd.DataFrame(people)
        batches_df = pd.DataFrame(batches)
        synthesis_df = pd.DataFrame(synthesis)
        parm_type_df = pd.DataFrame(parm_type)
        parameters_df = pd.DataFrame(parameters)
        values_df = pd.DataFrame(values)
        steps_df = pd.DataFrame(steps)
       

        people_df.to_sql('People1', con, if_exists='replace')
        batches_df.to_sql('Batches1', con, if_exists='replace')
        synthesis_df.to_sql('Synthesis1', con, if_exists='replace')
        parm_type_df.to_sql('Parm_type1', con, if_exists='replace')
        parameters_df.to_sql('Parameters1', con, if_exists='replace')
        values_df.to_sql('Parm_values1', con, if_exists='replace')
        steps_df.to_sql('Steps1', con, if_exists='replace')

        cur.executescript('''

        drop table if exists Parm_values;
        drop table if exists People;
        drop table if exists Batches;
        drop table if exists Synthesis;
        drop table if exists Parm_type;
        drop table if exists Parameters;
        drop table if exists Steps;

        create table Synthesis(syn_id INT PRIMARY KEY, description TEXT);
        create table Parm_type(type_id INT PRIMARY KEY, type TEXT);

        create table Parameters(par_id INT PRIMARY KEY, type_id INT, \
        description TEXT, FOREIGN KEY (type_id) REFERENCES Parm_type(type_id));

        create table People(owner_id INT PRIMARY KEY, description TEXT);

        create table Batches(batch_id TEXT PRIMARY KEY, item_name TEXT, syn_id\
            INT, owner_id, FOREIGN KEY (syn_id) REFERENCES Synthesis(syn_id),\
            FOREIGN KEY (owner_id) REFERENCES People(owner_id));

        create table Steps(syn_id INT, step_id INT PRIMARY KEY, par_id INT,\
            sequence INT, description TEXT,\
            FOREIGN KEY (syn_id) REFERENCES Synthesis(syn_id),\
            FOREIGN KEY (par_id) REFERENCES Parameters(par_id));

        create table Parm_values(batch_id INT, syn_id INT, step_id INT, \
            par_id INT, val,\
            FOREIGN KEY (batch_id) REFERENCES Batches(batch_id),\
            FOREIGN KEY (syn_id) REFERENCES Synthesis(syn_id),\
            FOREIGN KEY (step_id) REFERENCES Steps(step_id),\
            FOREIGN KEY (par_id) REFERENCES Parameters(par_id));

        insert into Parm_values select batch_id, syn_id, step_id, par_id, val \
            from Parm_values1;

        insert into People select owner_id, description from People1;
        insert into Batches select batch_id, item_name, syn_id, owner_id from \
        Batches1;
        insert into Synthesis select syn_id, description from Synthesis1;
        insert into Parm_type select type_id, type from Parm_type1;
        insert into Parameters select par_id, type_id, description from \
            Parameters1;
        insert into Steps select syn_id, step_id, par_id, sequence, \
            description from Steps1;

        drop table Parm_values1;
        drop table People1;
        drop table Batches1;
        drop table Synthesis1;
        drop table Parm_type1;
        drop table Parameters1;
        drop table Steps1
        ''')
