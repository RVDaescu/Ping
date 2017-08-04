import threading, string
from threading import Thread
from scapy.all import sniff, sendp, IP, ICMP, send
from random import choice

def raw(int):
    return ''.join(choice(string.uppercase) for i in range(int))
    

class snf(Thread):

    def __init__(self,output = [], filter = 'icmp', iface = 'enp2s0', count = -1, timeout = 30):

        """
        Constructor
        """

        Thread.__init__(self)

        self.output = output
        self.filter = filter
        self.iface = iface
        self.count = count
        self.timeout = timeout

    def run(self):
        """
        Thread run method
        """
        snf = sniff(filter = self.filter, iface = self.iface, count = self.count,
                    timeout = self.timeout)
        self.output.extend(snf)
        if len(snf) != 0:
            print 'Sniff on %s made; captured %d packets' %(self.iface, len(snf))
        else:
            print 'No packets captured with selected filter'

class snd(Thread):

    def __init__(self, host = '8.8.8.8', count = 10, iface = 'enp2s0', inter = 0.5, size = 32):

        """
        Constructor
        """

        Thread.__init__(self)

        self.host = host
        self.count = count
        self.iface = iface
        self.inter = inter
        self.size = raw(size) 

    def run(self):
        """
        Thread run method
        """
        
        packet = (IP(dst = self.host)/ICMP()/self.size)
        send(packet, iface = self.iface, count = self.count, inter = self.inter)

def main(list):
    
    ip = open(list, 'r')    

    ip_list = []

    for i in range(len(open(list, 'r').readlines())):
            ip_list.append(ip.readline().replace('\n', ''))
 
    for i in range(len(ip_list)):
        pkt_list = []
        print 'Starting sniff for %s' %ip_list[i]
        sniff_get = snf(output = pkt_list, filter = 'ip src %s and icmp' %ip_list[i])
        sniff_get.start()

        print 'Sending ICMP requests to %s' %ip_list[i]
        send_pk = snd(host = ip_list[i], size = 320)
        send_pk.start()

        sniff_get.join()
        send_pk.join()
    
    print pkt_list        
    return pkt_list

if __name__ in '__main__':
    if len(main('ip.txt')) != 10:
        print "Fail!"
    else:
        print 'Test passed'
