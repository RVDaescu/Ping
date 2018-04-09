#!/usr/bin/env python

from plot import plot

db = 'host_gns.sqlite'
tb = 'tb_8_8_8_8'

plot(db = db, tb = tb, pkt_loss = False, mode = 'fractile_25')
