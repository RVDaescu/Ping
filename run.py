#!/usr/bin/env python

from _config import database, table
from main import host
from sql_lib import sql
import sys

sys.dont_write_bytecode = True

"""Test case with local and remote IP's
"""

class main():
    
    db = database       
    tb = table      
    res_db = result_db

    list = sql().get_data(db = db, tb = tb, key = 'ip')

    hd = list.pop(0)

    for i in list:
        a = host(host = i[hd['IP']], db = res_db,
                read_db = db, read_tb = tb, 
                pkt_count = i[hd['pkt_count']], 
                pkt_inter = i[hd['pkt_inter']], 
                inter = i[hd['interval']])
        a.start()

if __name__ == '__main__':
    main()
