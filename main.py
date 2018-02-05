import threading
from threading import Thread

from time import sleep, ctime
from traffic import *
from sql_lib import *
from mail import *

class host(Thread):

    def __init__(self, ip, db, read_db, read_tb, pkt_count, pkt_inter, 
                 debug = False, link_dgr = False, inter = 3):
    
        Thread.__init__(self)

        self.host = ip              #IP to interogate
        self.db = db                #SQL db to write in; table will take host ip
        self.read_db = read_db      #sql db where monitoring status for IP is found
        self.read_tb = read_tb      #sql table where IP is found
        self.pkt_count = pkt_count  #number of packets to send on a request
        self.pkt_inter = pkt_inter  #interval between each packeta
        self.inter = inter          #interval between pols
        self.debug = debug          #print specific info
        self.link_dgr = link_dgr    #min percentage on which to notify the user on

    def run(self):
        Thread.run(self)
        down = False
        down_nr = 0
        lnk_dgr = False

        a = 0

        run = sql().get_value(db = self.read_db, tb = self.read_tb, field = 'Monitoring',
                              value = self.host, lookup = 'IP')

        while run == 'True':
            host_dict = {}
            table = 'tb_%s' %self.host.replace('.', '_')

            host_data = traffic(ip = self.host, count = self.pkt_count, 
                                inter = self.pkt_inter, debug = self.debug, 
                                out_dict = host_dict)

            host_data.start()
            host_data.join()
            
            write = sql()

            write.add_value(db = self.db, tb = table, **host_dict)
     
            if self.link_dgr:
                if host_dict['Reachability'] < self.link_dgr and lnk_dgr is False:
                    send_mail(msg = 'Host %s Minor alarm: Link degradation \n\n Host %s \n Time: %s \n Reachability: %r' \
                              %(self.host, self.host, ctime(host_dict['Time']), host_dict['Reachability']))
                    lnk_dgr = True
                
                elif host_dict['Reachability'] < minor_alarm and lnk_dgr is True:
                    pass

                elif host_dict['Reachability'] > minor_alarm and lnk_dgr is True:
                    lnk_dgr = False

            if host_dict['Reachability'] == 0 and down is False:
                down_nr +=1
                if down_nr == 3:
                    send_mail(msg = 'Host %s Critical alarm: DOWN \n\n Host %s \n Down Time: %s' \
                              %(self.host, self.host, ctime(host_dict['Time'])))
                    down = True
            
            elif host_dict['Reachability'] != 0 and down is False:
                down_nr = 0

            elif host_dict['Reachability'] != 0 and down is True:
                send_mail(msg = 'Host %s Critical alarm: CLEARED \n\n Host %s \n UP Time: %s' \
                          %(self.host, self.host, ctime(host_dict['Time'])))
                down_nr = 0
                down = False

            sleep(self.inter - self.pkt_count * self.pkt_inter)

            a += 1
