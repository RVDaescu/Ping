#!/usr/bin/env python

from _config import *
from main import monitor
from sql_lib import sql
from time import time,ctime,sleep
import sys

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
        if i[hd['Monitoring']]:
            a = monitor(host = i[hd['IP']],
                        pkt_count = i[hd['pkt_count']],
                        pkt_inter = i[hd['pkt_inter']],
                        inter = i[hd['interval']],
                        name = i[hd['Name']],
                        db = res_db)
            host_threads.append(a)
            a.start()
            sleep(0.1)
            started+=1
            if started % 10 == 0:
                sleep(1)

    sleep(30)
    for j in host_threads:
        print j

if __name__ == '__main__':
    main()
