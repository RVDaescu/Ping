#!/usr/bin/env python

from threading import enumerate as en
from _config import *
from main import monitor
from sql_lib import sql
from time import time,ctime,sleep
import sys

sys.dont_write_bytecode = True

class main():
    
    db = 'hosts_test.sqlite'  
    tb = 'group_01'
    res_db = 'res_test.sqlite'

    list = sql().get_data(db = db, tb = tb, key = 'ip')

    hd = list.pop(0)

    to_run = []        #list of running hosts
    to_stop = []        #list of stopped hosts
    run_threads = []    #list of threads started

    for i in list:
        if i[hd['Monitoring']] == 'True':
            a = monitor(host = i[hd['IP']],
                        pkt_count = i[hd['pkt_count']],
                        pkt_inter = i[hd['pkt_inter']],
                        inter = i[hd['interval']],
                        name = i[hd['Name']],
                        db = res_db)
            to_run.append(i)
            a.start()
            run_threads.append(a)
            sleep(0.05)
            if len(to_run) % 10 == 0:
                sleep(1)
        elif i[hd['Monitoring']] == 'False':
            to_stop.append(i)

    sleep(30)
    while True:
        list = sql().get_data(db = db, tb = tb, key = 'ip')
        hd = list.pop(0)
        
        for host in list:
            if host[hd['Monitoring']] == 'True' and host in to_stop:
                to_run.append(to_stop.pop(host))
            elif host[hd['Monitoring']] == 'False' and host in to_run:
                to_stop.append(to_run.pop(host))
            elif host[hd['Monitoring']] == 'True' and host not in to_run:
                to_run.append(host)           
            elif host[hd['Monitoring']] == 'False' and host not in to_stop:
                to_stop.append(host)
       
        for thread in run_threads:
            for stp in to_stop:
                if thread.name in stp:
                    thread.work = False
                    run_threads.pop(run_threads.index(thread)) 
        
        run_threads_name = [t.name for t in run_threads]

        for st in to_run:
            if st not in run_threads_name:
		a = monitor(host = st[hd['IP']],
			    pkt_count = st[hd['pkt_count']],
			    pkt_inter = st[hd['pkt_inter']],
			    inter = st[hd['interval']],
			    name = st[hd['Name']],
			    db = res_db)
		a.start()
		run_threads.append(a)
		sleep(0.1)
	sleep(60)

if __name__ == '__main__':
    main()
