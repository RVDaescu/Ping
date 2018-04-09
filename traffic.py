#!/usr/bin/env python

import threading, string, statistics, datetime, os
from threading import Thread
from scapy.all import sniff, sendp,Ether, IP, ICMP, wrpcap
from time import sleep, time
from utils import raw, ip_to_dev, ip_to_gw

import sys

sys.dont_write_bytecode = True

"""
objects for sniff and send traffic
"""

class snf(Thread):
    """
    Thread for sniffing traffic;
    """

    def __init__(self, output = [], filter = 'icmp', iface = None, 
                 count = -1, timeout = 10, debug = False):
        """
        output  : is a list with captured packets
        filter  : filter (BSF type) which will be applied to capture packets
        iface   : interface on which sniffing will be made
        count   : number of packets to capture
        timeout : durration of sniff
        debug   : stdout/info with sniffing results
        """
        
        #Constructor
        
        Thread.__init__(self)

        self.output = output
        self.filter = filter
        self.iface = iface
        self.count = count
        self.timeout = timeout
        self.debug = debug

    def run(self):
        """
        Starting thread with packet capture
        """
        #Sniff run method
        snf = sniff(filter = self.filter, iface = self.iface, 
                    count = self.count, timeout = self.timeout)
        self.output.extend(snf)

        if self.debug:
            if len(snf) != 0:
                print 'On interface %s %d packets were captured' \
                        %(self.iface, len(snf))
            else:
                print 'No packets captured with selected filter on interface %s' \
                        %self.iface
        self.stop()

    def stop(self):

        self._Thread__stop()
        return True

class snd(Thread):
    """
    Thread for sending traffic/packets
    """
    
    def __init__(self, host = '8.8.8.8', count = 10, iface = None, 
                 inter = 0.5, verbose = False):
        """
        host    : ip to which traffic is sent to
        count   : number of packets to send
        iface   : outgoing interface (will be determined based on host/IP
        inter   : interval between packets
        verbose : stdout/info with sent traffic
        """
        
        #Constructor

        Thread.__init__(self)

        self.host = host
        self.count = count
        self.iface = iface if iface else ip_to_dev(host)
        self.inter = inter
        self.verbose = verbose
    
    def run(self):
        """
        Starting thread with traffic sent
        """

        #Pkt send run method
        pkt_send_list = []
        load = Ether(dst = ip_to_gw(self.host))/\
               IP(dst = self.host)
        for i in range(self.count):
            pkt_send_list.append(load/ICMP(seq = i+1)) 
        
        sendp(pkt_send_list, iface = self.iface, 
             inter = self.inter, verbose = self.verbose)

        self.stop()

    def stop(self):

        self._Thread__stop()
        return True

class traffic(Thread):
    """
    Combined thread with sending and received traffic; 
    returns dictionary with reachability, avg rsp time jitter and 
        epoch time when the first packet was sent
    """

    def __init__(self, host, count = 10, inter = 1, 
                 iface = None, out_dict = {}, debug = False):
        """
        out_dict: returned dict by object; detailed bellow  
        ip      : ip/host (a.b.c.d) to run object on
        inter   : interval between packets
        iface   : interface on which traffic is sent/captured
        debug   : stdout with various infos on how the proccess is working
        """
        Thread.__init__(self)

        self.out_dict = out_dict                        #{}
        self.host = host                                #string *.*.*.*
        self.count = count                              #int
        self.inter = inter                              #float
        self.iface = iface if iface else ip_to_dev(host)  #string - outgoing interface for sending/receiving trafic
        self.debug = debug

    def run(self):
        """
        For ip (a.b.c.d) send traffic and than sniff packets according to filter
        Calculate and return ip_dict (contains - reachability, jitter, thread start time, latency, packet loss)
        """
        
        ip_dict = {}        #it will contain various informations - will be the return variable
        self.pkt_rv_list = []    #is the list with the ICMP reply packets
        self.pkt_st_list = []    #is the list with the ICMP request packets (needed for the .time)
        rsp_time = {}       #the dict with the response times for every ICMP echo (ms)
     
        ip_dict['Time'] = float(format(time(), '.2f'))
            
        #sniifing sent & recieved packets in order to get time out of them
        sniff_get_rv = snf(output = self.pkt_rv_list, 
                           filter = 'ip src %s and icmp' %self.host, 
                           iface= self.iface, 
                           timeout = self.count*self.inter*5,
                           debug = self.debug)
        sniff_get_rv.start()
       
        sniff_get_st = snf(output = self.pkt_st_list, 
                           filter = 'ip dst %s and icmp' %self.host,
                           iface = self.iface, 
                           timeout = self.count*self.inter*2+1,
                           debug = self.debug)
        sniff_get_st.start()

        if self.debug:
            print 'Sending ICMP requests to %s' %self.host
        
        send_pk = snd(host = self.host, iface = self.iface, 
                      count = self.count, inter = self.inter, 
                      verbose = self.debug)
        
        sleep(1)        #needed for packet build-up
        send_pk.start()
        
        send_pk.join()
        
        sniff_get_rv.join()
        sniff_get_st.join()

        seq_dict = {}   #contains the sequence dict from the response ICMP times 
                            #based on their sequence numbers 

        if not self.pkt_rv_list or (len(self.pkt_st_list) > len(self.pkt_rv_list)):
            """In case of some error, build out_dict with all value 0
            """
            ip_dict['Reachability'] = 0.0
            ip_dict['Jitter'] = 0.0
            ip_dict['Latency'] = 0.0
            ip_dict['Pkt_loss'] = 100.0
        
        elif not self.pkt_st_list:
            print "Error: No packets were sent!"
            return False

        else:

            #considering echo(s) was/were received
            ip_dict['Reachability'] = 100
            ip_dict['Pkt_loss'] = 100 - float(format(len(self.pkt_rv_list)/float(self.count)*100, '.2f'))
            
            for i in self.pkt_rv_list:
                seq_dict[int(i[ICMP].seq)] = i.time
            
            for i in range(self.count):
                if i+1 not in seq_dict.keys():
                    rsp_time[i+1] = 0 
                
                else:
                    try:
                        rsp_time[i+1] = float(format((seq_dict[i+1] - self.pkt_st_list[i].time)*1000, '.2f'))
                    except Exception, e:
                        cwd = os.getcwd()
                        wrpcap(cwd + '/logs/%s_%s.pcap' %(self.host, time()), self.pkt_rv_list+self.pkt_st_list) 
                        print "sent pkt list len: %d \n recevied pkt list len: %d \n seq_dict: %s" \
                              %(len(self.pkt_st_list), len(self.pkt_rv_list), seq_dict)
                        print e

            ip_dict['Latency'] = float(format(statistics.mean(rsp_time.values()), '.2f'))
            ip_dict['Jitter'] = float(format(statistics.stdev(rsp_time.values()), '.2f'))

        self.out_dict.update(ip_dict)

        self.stop()

    def stop(self):

        self._Thread__stop()
        return True
