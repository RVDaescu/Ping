#!/usr/bin/env python
from threading import Thread
from _config import dbs
from main import monitor
from sql_lib import sql
from time import sleep
import sys, threading

sys.dont_write_bytecode = True

class main(Thread):

    def __init__(self, sql_db, sql_tb, res_sql, down_nr):
        
        Thread.__init__(self)
        self.sql_db = sql_db
        self.sql_tb = sql_tb
        self.res_sql = res_sql

    def run(self):

        list_from_db = sql().get_data(db = self.sql_db, 
                                      tb = self.sql_tb,
                                      key = 'ip')
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
                            down_nr = down_nr,
                            db = self.res_sql)
                print 'starting %s' %i[hd['Name']]
                a.start()
                to_run.append(i[hd['Name']])
                run_threads.append(a)
                sleep(0.1)
                if len(to_run) % 10 == 0:
                    sleep(1)
            elif i[hd['Monitoring']] == 'False':
                to_stop.append(i[hd['Name']])

        sleep(30)
        while True:
            list_from_db = sql().get_data(db = self.sql_db, 
                                          tb = self.sql_tb, 
                                          key = 'ip')
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
                
                for th in run_threads:
                    if host[hd['Monitoring']] == 'True' and th.isAlive() is False:
                        run_threads.pop(run_threads.index(th))
                        a1 = monitor(host = host[hd['IP']],
                                    pkt_count = host[hd['pkt_count']],
                                    pkt_inter = host[hd['pkt_inter']],
                                    inter = host[hd['interval']],
                                    name = host[hd['Name']],
                                    down_nr = down_nr,
                                    db =self.res_sql)
                        a1.start()
                        sleep(0.1) 
                        run_threads.append(a1)

            for thread in run_threads:
                if run_threads.count(thread) != 1:
                    thread.work = False
                for stp in to_stop:
                    if thread.name == stp:
                        thread.work = False
                        print 'Stopping %s' %thread.name
                        sleep(1)
                        run_threads.pop(run_threads.index(thread)) 
            
            for strt in to_run:
                if strt not in [i.name for i in run_threads]:
                    for host in list_from_db:
                        if host[hd['Name']] == strt:
                            b = monitor(host = host[hd['IP']],
                                        pkt_count = host[hd['pkt_count']],
                                        pkt_inter = host[hd['pkt_inter']],
                                        inter = host[hd['interval']],
                                        name = host[hd['Name']],
                                        down_nr = down_nr,
                                        db = self.res_sql)
                            b.start()
                            print 'Started thread %s' %i[hd['Name']]
                            run_threads.append(b)

            sleep(180)

for database in dbs.keys():
    for data in dbs[database]:
        db = database
        tb = data['table']
        res_db = data['results']
        down_nr = data['down_nr']
        th = main(sql_db = db, sql_tb = tb, res_sql = res_db, down_nr = down_nr)
        th.start()
