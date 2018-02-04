#!/usr/bin/env python

from main import host
from sql_lib import sql

"""Test case with local and remote IP's
"""

status = True
db = 'hosts.sqlite'

while True:

    list = sql().get_data(db = db, tb = 'group_01', key = 'ip')

    hd = list.pop(0)

    for i in list:
        if i[hd['Monitoring']] is True:
            a = host(ip = i['IP'], db = db, 
                pkt_count = i['pkt_count'], 
                pkt_inter = i['pkt_inter'], 
                inter = i['interval'], 
                repeat_nr = 1000, 
                debug = False,
            a.start()  

    #for i in ip:
    #    a = host(ip = i, db = db, pkt_count = 3, pkt_inter = 1, 
    #             inter = 10, repeat_nr = 1000, debug = False)
    #    a.start()
