#!/usr/bin/env python

from threading import enumerate as en
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

    list_from_db = sql().get_data(db = db, tb = tb, key = 'ip')
    hd = list_from_db.pop(0)

    to_run = []         #list of running hosts
    to_stop = []        #list of stopped hosts
    run_threads = []    #list of threads started

    for i in list_from_db:
        if i[hd['Monitoring']] == 'True':
            a = monitor(host = i[hd['IP']],
                        pkt_count = i[hd['pkt_count']],
                        pkt_inter = i[hd['pkt_inter']],
                        inter = i[hd['interval']],
                        name = i[hd['Name']],
                        db = res_db)
            to_run.append(i[hd['Name']])
            a.start()
            run_threads.append(a)
            sleep(0.05)
            if len(to_run) % 10 == 0:
                sleep(1)
        elif i[hd['Monitoring']] == 'False':
            to_stop.append(i[hd['Name']])

    sleep(30)
    while True:
        list_from_db = sql().get_data(db = db, tb = tb, key = 'ip')
        hd = list_from_db.pop(0)
        
        for host in list_from_db:
            if host[hd['Monitoring']] == 'True' and host[hd['Name']] in to_stop:
                to_run.append(to_stop.pop(to_stop.index(host[hd['Name']])))
            elif host[hd['Monitoring']] == 'False' and host[hd['Name']] in to_run:
                to_stop.append(to_run.pop(to_run.index(host[hd['Name']])))
            elif host[hd['Monitoring']] == 'True' and host[hd['Name']] not in to_run:
                to_run.append(host[hd['Name']]) 
            elif host[hd['Monitoring']] == 'False' and host[hd['Name']] not in to_stop:
                to_stop.append(host[hd['Name']])
      
        for thread in run_threads:
            for stp in to_stop:
                if thread.name == stp:
                    thread.work = False
                    sleep(1)
                    run_threads.pop(run_threads.index(thread)) 
        
        run_threads_name = [t.name for t in run_threads]
        
        for strt in to_run:
            if strt not in run_threads_name:
                for host in list_from_db:
                    if host[hd['Name']] == strt:
                        a = monitor(host = host[hd['IP']],
                                    pkt_count = host[hd['pkt_count']],
                                    pkt_inter = host[hd['pkt_inter']],
                                    inter = host[hd['interval']],
                                    name = host[hd['Name']],
                                    db = res_db)
                        a.start()
                        run_threads.append(a)
	sleep(30)

if __name__ == '__main__':
    main()
