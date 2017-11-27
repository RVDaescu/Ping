#!/usr/bin/env python

from main import host

ips = open('ip.txt', 'r').readlines()
ip = [i.strip('\n') for i in ips]

for i in ip:
    a = host(ip = i, db = 'host_gns.sqlite', pkt_count = 3, 
             pkt_inter = 1, inter = 10, repeat_nr = 1000, debug = False)
    a.start()
