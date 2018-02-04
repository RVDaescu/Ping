from random import choice
from sql_lib import sql
"""
simple method to populate a sql with hosts
"""
dbd = sql()
db = 'hosts.sqlite'
tb = 'group_01'                                                                     
                
f = open('ip.txt', 'r')
ips = [i.replace('\n','') for i in f.readlines()]

for i in ips:
    hs = {'IP': i, 'pkt_count': choice([3,4,5]), 
          'pkt_inter' : choice([1,1.5,2]), 
          'interval' : choice(range(180,300,30)),
          'Monitoring': choice([True,False])}
    dbd.add_value(db = db, tb = tb, **hs)

