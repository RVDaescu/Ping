#!/usr/bin/env python
from gnu import *
from time import sleep


ip1 = ['10.10.108.1','10.10.108.2','10.10.109.1','10.10.109.2','89.47.247.29','185.60.216.35','172.217.16.99','172.217.16.110','185.133.64.69','216.58.209.163']
ips = ['92.123.37.254']
for ip in ips:
    for mod in ['min','max','average','fractile_50']:
        tb = 'tb_'+ip.replace('.','_')
        plot_to_file(db = 'results.sqlite',tb = tb, mode = mod)
