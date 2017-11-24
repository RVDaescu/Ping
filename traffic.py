#!/usr/bin/env python

import threading, string, statistics, datetime
from threading import Thread
from scapy.all import sniff, send, IP, ICMP 
from time import sleep, time
from utils import raw
 
class snf(Thread):

    def __init__(self, output = [], filter = 'icmp', iface = 'wlo1', 
                 count = -1, timeout = 10, debug = False):
        #Constructor
        
        Thread.__init__(self)

        self.output = output
        self.filter = filter
        self.iface = iface
        self.count = count
        self.timeout = timeout
        self.debug = debug

    def run(self):
        #Sniff run method
        snf = sniff(filter = self.filter, iface = self.iface, 
                    count = self.count, timeout = self.timeout)
        self.output.extend(snf)
        
        if self.debug:
            if len(snf) != 0:
                print 'Sniff on %s made; captured %d packets' \
                        %(self.iface, len(snf))
            else:
                print 'No packets captured with selected filter'

class snd(Thread):
    
    def __init__(self, host = '8.8.8.8', count = 10, iface = 'wlo1', 
                 inter = 0.5, verbose = False):
        #Constructor

        Thread.__init__(self)

        self.host = host
        self.count = count
        self.iface = iface
        self.inter = inter
        self.verbose = verbose
    
    def run(self):
        #Pkt send run method
        
        pkt_send_list = []
        load = IP(dst = self.host)
        for i in range(self.count):
            pkt_send_list.append(load/ICMP(seq = i+1)) 

        send(pkt_send_list, iface = self.iface, inter = self.inter, verbose = self.verbose)

class traffic(Thread):

    def __init__(self, ip, count = 10, inter = 1, port = None, out_dict = {}, debug = False):

        Thread.__init__(self)

        self.out_dict = out_dict                        #{}
        self.ip = ip                                    #string *.*.*.*
        self.count = count                              #int
        self.inter = inter                              #float
        self.port = ip_to_dev(ip) if None else port     #string - outgoing interface for sending/receiving trafic
        self.debug = debug

    def run(self):
        """
        Descr: for ip (string) sniff packets according to filter
               - return ip_dict (contains -reachability, jitter, pkts sent/received, thread start time)
        """
        
        ip_dict = {}        #it will contain various informations - will be the return variable
        pkt_rv_list = []    #is the list with the ICMP response packets
        pkt_st_list = []    #is the list with the ICMP request packets (needed for the .time)
        rsp_time = {}       #the dict with the response times for every ICMP echo (ms)
     
        ip_dict['Time'] = float(format(time(), '.2f'))
       
        #sniifing sent & recieved packets in order to get time out of them
        sniff_get_rv = snf(output = pkt_rv_list, filter = 'ip src %s and icmp[icmptype] == 0' %self.ip, 
                        iface= self.port, count = self.count, timeout = self.count*self.inter*2+1,
                        debug = self.debug)
        sniff_get_rv.start()
 
        sniff_get_st = snf(output = pkt_st_list, filter = 'ip dst %s and icmp[icmptype] == 8' %self.ip,
                         iface = self.port, count = self.count, timeout = self.count*self.inter*2+1,
                         debug = self.debug)
        sniff_get_st.start()

        #print 'Sending ICMP requests to %s' %self.ip
        send_pk = snd(host = self.ip, iface = self.port, count = self.count, 
                      inter = self.inter, verbose = self.debug)
        sleep(1)
        send_pk.start()
        
        send_pk.join()

        seq_dict = {}   #contains the sequence dict from the response ICMP times 
                            #based on their sequence numbers 

        if not (pkt_st_list or pkt_rv_list) or (len(pkt_rv_list) > len(pkt_st_list)):
            ip_dict['Reachability'] = 0.0
            ip_dict['Jitter'] = 0.0
            ip_dict['Avg_Rsp_time'] = 0.0
        
        else:
            for i in range(len(pkt_rv_list)):
                seq_dict[pkt_rv_list[i][ICMP].seq] = pkt_rv_list[i].time

            ip_dict['Reachability'] = float(format(len(pkt_rv_list)/float(self.count)*100, '.2f'))

            for i in range(self.count):
                if i+1 not in seq_dict.keys():
                    rsp_time[i+1] = 0 
                elif pkt_st_list:
                    try:
                        rsp_time[i+1] = float(format((seq_dict[i+1] - pkt_st_list[i].time)*1000, '.2f'))
                    except Exception, e:
                        print len(pkt_st_list), len(pkt_rv_list), len(seq_dict)
                        print e

            #ip_dict['rsp_dict']

            ip_dict['Avg_Rsp_time'] = float(format(statistics.mean(rsp_time.values()), '.2f'))
            ip_dict['Jitter'] = float(format(statistics.stdev(rsp_time.values()), '.2f'))

        self.out_dict.update(ip_dict)
