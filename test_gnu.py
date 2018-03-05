#!/usr/bin/env python

from gnu import *
import sys

sys.dont_write_bytecode = True

db = 'res_db.sqlite'
ip = '8.8.8.8'

#start = '16/02/18-08:00:00'
#end = '17/02/18-14:00:00'

for f in ['Reachability', 'Jitter', 'Latency', 'Pkt_loss']:
    plot_to_file(db = db, tb = 'tb_'+ip.replace('.','_'), field = f)
