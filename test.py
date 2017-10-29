#!/usr/bin/env python

from main import host

host(host ='8.8.8.8', db_name = 'host.sql', pkt_count = 3, pkt_inter = 0.1, interval =3, repeat_nr = 100000)
