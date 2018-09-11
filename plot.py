#!/usr/bin/env python

from graphic import *

import sys, argparse

parser=argparse.ArgumentParser()

parser.add_argument('-db', help ='SQL db where the table is in')
parser.add_argument('-tb', help ='SQL tb where the data is to be ploted')
parser.add_argument('-rc', default = False, help ='Plot reachability?')
parser.add_argument('-pl', default = False, help ='Plot packet loss?')
parser.add_argument('-jt', default = False, help ='Plot jitter?')
parser.add_argument('-lt', default = False, help ='Plot latency?')
parser.add_argument('-st', default = None, help ='Start time for data')
parser.add_argument('-en', default = None, help ='End time for data')
parser.add_argument('-name', help ='Start time for data')
parser.add_argument('-mode', default = 'average', help ='Mode for plotting data ')

args=parser.parse_args()

create_graphic(db = args.db, tb = args.tb, 
               reach = args.rc, pkt_loss = args.pl, 
               jitter = args.jt, latency = args.lt,
               start = args.st, end = args.en, 
               mode = args.mode, name = args.name, dpi = 200)
