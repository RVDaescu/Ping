#!/usr/bin/env python

from main import host

ips = open('ip2.txt', 'r').readlines()
ip = [i.strip('\n') for i in ips]

for i in ip:
    a = host(ip = i, db_name = 'host_gns.sqlite', pkt_count = 3, pkt_inter = 1, inter = 5, repeat_nr = 5, debug = False)
    a.start()
