# -*- coding: utf-8 -*-
"""
Created on Fri May 15 07:51:35 2015

@author: Neill
"""

import re
import pandas as pd


name_file = ['Ca/Mg/Zn','Portlanite','Dolomite', 'CalMag', 'Meix', 'HTC', ' Meixnerite', 'Ca:Mg', 'Mg/Ca', 'meix' ]
ca_matcher = re.compile('(Ca\\b|Ca\\d|Ca[^O,o,r,l,t]|CalMag|Calcium|Lime\
                     |Katoite|kat|Hydrocalumite|Portlanite|\
                     Dolomite)', re.IGNORECASE)

         
mg_matcher = re.compile('(Mg|Mg\\b|Mg\\d|Mg[^O,o]|CalMag|Magnesium\
                         |Bricite|Meixnerite|HTC|Hydrotalcite|\
                         Dolomite|Pyrosorb|Alcimazer|Meix)',re.IGNORECASE)
                         



for line in name_file:
    m_ca = ca_matcher.search(line.strip())
    m_mg = mg_matcher.search(line.strip())
    
    print line.strip()
    print 'match ca',m_ca
    print 'match mg',m_mg
#    print m_ca.groups(), m_mg.groups()
    
    if m_ca and m_mg:
        ca = 1
        mg = 1
        print m_ca.groups(), m_mg.groups()
        
    elif m_ca or m_mg:
        if m_ca:
            print m_ca.groups()
            ca = 1
        elif not m_ca:
            ca = 0
            
        if m_mg:
            mg = 1
            print m_mg.groups()
        elif not m_mg:
            mg = 0
        
    elif not m_ca and not m_mg:
        ca = 0
        mg = 0          
            
    print 'Ca', 'Mg'
    print ca, mg
    print
    


    
