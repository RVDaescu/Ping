import threading, string, statistics, datetime
from threading import Thread
from scapy.all import sniff, send, IP, ICMP 
from random import choice
from time import sleep, time

def raw(int):
    return ''.join(choice(string.lowercase) for i in range(int))
    

class snf(Thread):

    def __init__(self,output = [], filter = 'icmp', iface = 'wlo1', count = -1, timeout = 10):
        #Constructor
        
        Thread.__init__(self)

        self.output = output
        self.filter = filter
        self.iface = iface
        self.count = count
        self.timeout = timeout

    def run(self):
        #Sniff run method
        snf = sniff(filter = self.filter, iface = self.iface, count = self.count,
                    timeout = self.timeout)
        self.output.extend(snf)
        if len(snf) != 0:
            print 'Sniff on %s made with filter(%s) ; captured %d packets' %(self.iface, self.filter, len(snf))
        else:
            print 'No packets captured with selected filter'

class snd(Thread):

    def __init__(self, host = '8.8.8.8', count = 10, iface = 'enp2s0', 
                 inter = 0.5, size = 32, seq = 0):
        #Constructor

        Thread.__init__(self)

        self.host = host
        self.count = count
        self.iface = iface
        self.inter = inter
        self.size = raw(size) 
        self.seq = seq

    def run(self):
        #Pkt send run method
        
        pkt_send_list = []
        for i in range(self.count):
            pkt_send_list.append(IP(dst = self.host)/ICMP(seq = i+1)/self.size)

        send(pkt_send_list, iface = self.iface, inter = self.inter)

def main(ip, count = 100, inter = 0.01):
    """
    Descr: for ip (string) sniff packets according to filter
           - return ip_dict (contains various informations)
    """
    ip_dict = {}        #it will contain various informations - will be the return variable
    pkt_list = []       #is the list with the ICMP response packets
    pkt_st_list = []    #is the list with the ICMP request packets (needed for the .time)
    rsp_time = {}       #the dict with the response times for every ICMP echo (ms)
 
    ip_dict['time'] = format(time(), '.2f')
   
    print 'Starting sniff for %s' %ip
    sniff_get = snf(output = pkt_list, filter = 'ip src %s and icmp' %ip, 
                    iface= 'wlo1', timeout = count*inter*2+1)
    sniff_get.start()
    sniff_get1 = snf(output = pkt_st_list, filter = 'ip dst %s and icmp' %ip,
                     iface = 'wlo1', timeout = count*inter*2+1)
    sniff_get1.start()


    print 'Sending ICMP requests to %s' %ip
    send_pk = snd(host = ip, size = 32, iface = 'wlo1', count = count, inter = inter)
    sleep(1)
    send_pk.start()
    
    send_pk.join()
    sniff_get.join()
    sniff_get1.join()

    seq_dict = {}   #contains the sequence dict from the response ICMP times 
                        #based on their sequence numbers 
    for i in range(len(pkt_list)):
        seq_dict[pkt_list[i][ICMP].seq] = pkt_list[i].time

    ip_dict['received'] = len(pkt_list)
    ip_dict['sent'] = count
    ip_dict['reach'] = str(format(float(len(pkt_list))/float(count)*100, '.2f')+ ' %')

    for i in range(count):
        if i+1 not in seq_dict.keys():
            rsp_time[i+1] = 0 
        else:
            rsp_time[i+1] = float(format((seq_dict[i+1] - pkt_st_list[i].time)*1000, '.2f'))
    
    ip_dict['rsp_dict'] = rsp_time

    ip_dict['avg_rsp'] = float(format(statistics.mean(rsp_time.values()), '.2f'))
    
    ip_dict['jitter'] = float(format(statistics.stdev(rsp_time.values()), '.2f'))

    return ip_dict

#if __name__ in '__main__':
#    print main('8.8.8.8', count = 5000, inter = 0.01)
