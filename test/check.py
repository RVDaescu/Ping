#!/usr/bin/env python

import sys
sys.path.append('/root/netmonpy/Ping')

from sql_lib import *
from utils import *

from time import time, ctime

db = 'res_db.sqlite'
tbs = get_sql_db_table(db = db)
failed = []
ts = []

tb = 'tb_imdb'

#print sql().get_data(db = db, tb = tb, field = 'time')[1:]

max_wait_time = 600

for tb in tbs:
    t = max(sql().get_data(db = db, tb = tb, field = 'Time')[1:])[0]
    if time() - t > max_wait_time:
        failed.append(tb)
        ts.append(ctime(t))

if len(ts) == 0:
    print "All the threads are working"

else:
    print "%s are not working for more than %s" %(len(failed), max_wait_time)
    for i,j in zip(failed,ts): 
        print "%s since \t\t %s" %(i,j)
