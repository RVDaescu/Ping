#!/usr/bin/env python

from main import host

ips = open('ip.txt', 'r').readlines()
ip = [i.strip('\n') for i in ips]

for i in ip:
    a = host(ip = i, db_name = 'host_gns.sqlite', pkt_count = 5, pkt_inter = 3, inter =300, repeat_nr = 1000)
    a.start()
