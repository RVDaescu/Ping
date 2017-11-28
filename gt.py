#!/usr/bin/env python
from gnu import *
from time import sleep


ips = ['10.10.108.1','10.10.108.2','10.10.109.1','10.10.109.2','89.47.247.29','185.60.216.35','172.217.16.99','172.217.16.110','185.133.64.69','216.58.209.163']
for ip in ips:
    for f in ['Reachability','Jitter','Avg_Rsp_time']:
        tb = 'tb_'+ip.replace('.','_')
        plot_to_file(db = 'host_gns.sqlite',tb = tb, field = f)
        sleep(0.6)
