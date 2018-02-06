#!/usr/bin/env python

from main import host
from sql_lib import sql

"""Test case with local and remote IP's
"""

class main():
    
    db = 'hosts.sqlite'
    tb = 'group_01'

    list = sql().get_data(db = db, tb = tb, key = 'ip')

    hd = list.pop(0)

    res_db = 'res_db.sqlite'

    for i in list:
        a = host(ip = i[hd['IP']], db = res_db,
                read_db = db, read_tb = tb, 
                pkt_count = i[hd['pkt_count']], 
                pkt_inter = i[hd['pkt_inter']], 
                inter = i[hd['interval']]/20)
        a.start()

if __name__ == '__main__':
    main()
