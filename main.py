from time import sleep
from traffic import *
from sql_lib import *

def traf2sql(host, db_name, pkt_count = 3, pkt_inter = 1, size = 32, interval = 10, repeat_nr = 10, loop = False):
    """
    method 
    """
    
    for i in range(repeat_nr):

        host_dict = {}
        table = 'table_%s' %host.replace('.', '_')

        host_data = main(host, count = pkt_count, inter = pkt_inter,out_dict = host_dict)

        host_data.start()
        host_data.join()

        sql_add_value(db_name = db_name, tb_name = table, **host_dict)

        sleep(interval)

