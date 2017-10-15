#!/usr/bin/env python

from time import sleep
from traffic import *
from sql_lib import *

def traf2sql(host_list, db_name, pkt_count = 3, pkt_inter = 1, size = 32, interval = 10, repeat_nr = 10):
    """
    method 
    """

    for i in range(repeat_nr):
        for host in host_list:
    
            host_dict = {}
            table = 'table_%s' %host.replace('.', '_')
            
            host_data = main(host, count = pkt_count, inter = pkt_inter,out_dict = host_dict)

            host_data.start()
            host_data.join()

            sql_add_value(db_name = db_name, tb_name = table, **host_dict)
            
            sleep(interval)

traf2sql(host_list = ['92.223.1.112'], db_name = 'host.sql', pkt_count = 10, pkt_inter = 0.1, interval =60, repeat_nr = 1000)


"""
for i in range(10):
    
    host1 = '192.168.1.152'
    table1 = 'table_%s' %host1.replace('.', '_')

    host2 = '8.8.8.8' 
    table2 = 'table_%s' %host2.replace('.', '_')
    
    db_name = 'host.sql'

    host_1_dict = {}
    host_2_dict = {}

    a = main(host1, count = 3, inter = 0.5, out_dict = host_1_dict)
    b = main(host2, count = 3, inter = 0.5, out_dict = host_2_dict)

    a.start()
    b.start()
    
    a.join()
    b.join()

    sql_add_value(db_name = db_name, tb_name = table1, **host_1_dict)
    sql_add_value(db_name = db_name, tb_name = table2, **host_2_dict)
   
    sleep(1)
"""
