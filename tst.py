#!/usr/bin/env python

from main import traf2sql

traf2sql(host = '92.223.1.112', db_name = 'host.sql', pkt_count = 2, pkt_inter = 0.1, interval =1, repeat_nr = 10000)


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
