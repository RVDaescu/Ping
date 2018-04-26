#!/usr/bin/env python

import sys
sys.path.append('/root/netmonpy/Ping')
from graphic import create_graphic

db = 'res_db.sqlite'
tb = 'global_dns'

for mod in ['average','max','min','fractile_50']:
    create_graphic(db = db, tb = tb, jitter = False, reach = False, mode = mod, start = '9/4/18-23:00:00')
