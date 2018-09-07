#!/usr/bin/env python

import os
cwd = os.getcwd()

import sys
sys.path.append(cwd)

from graphic import create_graphic
from utils import get_sql_db_table

db = 'res_interlan.sqlite'
#tb = ['vodafone_ro','gsp_ro']

tb = get_sql_db_table(db)

#tb = ['google_peer_interlan_ro']

for t in tb:
    for mod in [None]:
        create_graphic(db = db, tb = t, jitter = True, reach = True, 
                       latency = True, pkt_loss = True, mode = mod, 
                       start = '8/8/18-00:00:01')
