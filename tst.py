#!/usr/bin/env python

from traffic import *
from sql_lib import *

for i in range(10):
    
    host1 = '192.168.1.152'
    table1 = 'table_%s' %host1.replace('.', '_')

    host2 = '8.8.8.8' 
    table2 = 'table_%s' %host2.replace('.', '_')
    
    db_name = 'host.db'

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
