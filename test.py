#!/usr/bin/env python

from main import host

host(host ='8.8.8.8', db_name = 'host.sql', pkt_count = 3, pkt_inter = 1, interval =10, repeat_nr = 3)
