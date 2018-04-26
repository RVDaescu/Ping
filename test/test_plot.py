#!/usr/bin/env python

import sys
sys.path.append('/root/netmonpy/Ping')
from graphic import create_graphic

db = 'res_db.sqlite'
tb = 'cpanel_com'

for mod in [None,'average', 'fractile_05']:
    create_graphic(db = db, tb = tb, jitter = True, reach = True, mode = mod)
