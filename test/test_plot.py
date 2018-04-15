#!/usr/bin/env python

import sys
sys.path.append('/home/radu/Ping')
from plot import plot

db = 'res_db.sqlite'
tb = 'tb_global'

for mod in ['average','max','min','fractile_50']:
    plot(db = db, tb = tb, jitter = False, reach = False, mode = mod, start = '9/4/18-23:00:00')
