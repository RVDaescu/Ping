#!/usr/bin/env python

from _config import *
from main import monitor
from sql_lib import sql
import sys
from time import time,ctime

sys.dont_write_bytecode = True

class main():
    
    db = database       
    tb = table      
    res_db = result_db

    host_threads = []

    list = sql().get_data(db = db, tb = tb, key = 'ip')

    hd = list.pop(0)

    started = 0

    for i in list:
        a = monitor(host = i[hd['IP']], db = res_db,
                read_db = db, read_tb = tb)
        host_threads.append(a)
        a.start()
        sleep(0.1)
        started+=1
        if started % 10 == 0:
            sleep(1)

    for host in host_threads:
        if not host.isAlive()
            print '%s: %s' %(ctime(time()), host)
        host_threads.pop(host)

        sleep(600)

if __name__ == '__main__':
    main()
