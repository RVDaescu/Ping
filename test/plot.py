#!/usr/bin/env python

import os
cwd = os.getcwd()

import sys
sys.path.append(cwd)

from graphic import create_graphic
from utils import get_sql_db_table

db = 'res_interlan.sqlite'
db = 'res_db.sqlite'
#tb = ['vodafone_ro','gsp_ro']

tb = get_sql_db_table(db)

tb = ['google_dns_com','global2_dns']

for t in tb:
    for mod in [None]:
        create_graphic(db = db, tb = t, jitter = True, reach = False, 
                       latency = True, pkt_loss = False, mode = mod, 
                       start = '8/8/17-00:00:01')
