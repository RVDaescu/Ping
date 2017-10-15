#!/usr/bin/env python

from traffic import *
from sql_lib import *

for i in range(10):
    
    host = '151.101.129.12'
    table = 'table_' + str(host.replace('.', ''))
    db_name = 'host.db'

    a = main(host, size = 100, count = 10, inter = 0.1)
    sql_add_value(db_name = db_name, tb_name = table, **a)
    
    sleep(3)
