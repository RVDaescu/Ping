#!/usr/bin/env python

import os
cwd = os.getcwd()

import sys
#sys.path.append('/'.join(cwd.split('/')[:-1]))
sys.path.append(cwd)

from sql_lib import *
from utils import *
from _config import dbs
from time import time, ctime

hosts = []
res = []
for database in dbs.keys():
    hosts.append(database)
    for data in dbs[database]:
        res.append(data['results'])

        db = data['results'] 
        tbs = get_sql_db_table(db = db)
        failed = []
        ts = []

        #print sql().get_data(db = db, tb = tb, field = 'time')[1:]

        max_wait_time = 500

        for tb in tbs:
            t = max(sql().get_data(db = db, tb = tb, field = 'Time')[1:])[0]
            if time() - t > max_wait_time:
                failed.append(tb)
                ts.append(ctime(t))

        if len(ts) == 0:
#            print "All the threads are working in %s" %data['results']
            pass
        else:
            print "%s are not working for more than %s seconds in %s" %(len(failed), max_wait_time,data['results'])
            for i,j in zip(failed,ts): 
                print "\t%s since %s" %(i,j)

intr = {}
for host in hosts:
    for tbh in get_sql_db_table(db = host):
        dt = sql().get_data(db = host, tb=tbh, field='Name,interval,Monitoring',key='Name')
        for a,b,c in dt:
            if c == 'True':
                intr['%s' %a.replace('.','_')]=b

bad={}
for db in res:
    for tb in get_sql_db_table(db = db):
        data = sql().get_data(db = db, tb = tb, field = 'Time,Reachability', start = time()-24*3600)
        bad['%s' %tb] = {}
        if len(data) >3 and tb in intr.keys():
            hd=data.pop(0)
            for i,j in zip(data[:-1], data[1:]):
                if j[0] - i[0] +1 < intr[tb]:
                    bad['%s' %tb][i[0]]=j[0]-i[0]

for s,r in bad.items():
    if len(r) >2:
        print 'There are hosts who collect data multiple times ' \
              'in the past 24 hours: %s' %s
        print ctime(r.keys()[0])
        print ctime(r.keys()[-1])
