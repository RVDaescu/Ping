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

    counter = 0

    while True:
        
        list = sql().get_data(db = db, tb = tb, key = 'ip')

        hd = list.pop(0)

        for i in list:
            a = monitor(host = i[hd['IP']], db = res_db,
                    read_db = db, read_tb = tb)
            host_threads.append(a)
            a.start()

        counter +=1

        if counter == 10:
            for i in host_threads:
                print i
        print '%s: %s' %(ctime(time()), counter)

if __name__ == '__main__':
    main()
