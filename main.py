import threading
from threading import Thread

from time import sleep, ctime
from traffic import *
from sql_lib import *
from mail import *
import sys

sys.dont_write_bytecode = True


class host(Thread):

    def __init__(self, host, db, read_db, read_tb, debug = False, link_dgr = None):
    
        Thread.__init__(self)

        self.host = host            #IP to interogate
        self.db = db                #SQL db to write data in; table will take host ip
        self.read_db = read_db      #sql db where monitoring status for IP is found
        self.read_tb = read_tb      #sql table where IP is found
      
        #getting all the data from the SQL for the host 
        host_info = sql().get_row(db = self.read_db, tb = self.read_tb, lookup = self.host)

        #number of packets to send on a request
        self.pkt_count = host_info[1][host_info[0]['pkt_count']]
        
        #interval between each packet
        self.pkt_inter =  host_info[1][host_info[0]['pkt_inter']]
        
        #interval between polls
        self.inter = host_info[1][host_info[0]['interval']]
        
        #print specific info
        self.debug = debug 

        self.link_dgr = link_dgr    #min percentage on which to notify the user on the packet loss; if 'None' it's not ran
        self.name = ip_to_name(db = read_db, tb = read_tb, ip = host)     #name or NS of IP/host

    def run(self):
        
        Thread.run(self)
        
        down = False
        down_nr = 0
        inform = False
        dgr = False
        dgr_nr = 0

        if self.inter <= (self.pkt_count * self.pkt_inter)+2:
            print 'Interval between polls is smaller than the duration of the poll'
            return False

        run = sql().get_value(db = self.read_db, tb = self.read_tb, field = 'Monitoring',
                              value = self.host, lookup = 'IP')

        while run == 'True':
            
            host_dict = {}
            table = 'tb_%s' %self.name.split('.')[-2]

            host_data = traffic(host = self.host, count = self.pkt_count, 
                                inter = self.pkt_inter, debug = self.debug, 
                                out_dict = host_dict)

            host_data.start()
            host_data.join()
            
            sql().add_value(db = self.db, tb = table, **host_dict)

            if self.link_dgr:
                if host_dict['Pkt_loss'] >= self.link_dgr and link_dgr is False:
                    dgr_nr += 1
                    #after 5 consecutive degradations, send an email
                    if dgr_nr == 5:
                        send_mail(msg = 'Host %s  Minor alarm: Link degradation \n\n Host %s (%s) \n Time: %s \n Reachability: %r' \
                                  %(self.name, self.name, self.host, ctime(host_dict['Time']), host_dict['Reachability']))
                        link_dgr = True
                
                elif host_dict['Pkt_loss'] >= self.link_dgr and link_dgr is True:
                    pass

                elif host_dict['Reachability'] < self.link_dgr and link_dgr is True:
                    link_dgr = False
                    dgr_nr = 0

            if host_dict['Reachability'] == 0 and down is False:
                down_nr += 1
                if down_nr == 3:
                        send_mail(msg = 'Host %s Critical alarm: DOWN \n\n Host %s (%s) \n Down Time: %s' \
                                  %(self.name, self.name, self.host, ctime(host_dict['Time'])))
                        inform = True
                        down = True
            
            elif host_dict['Reachability'] != 0:
                down_nr = 0

            elif host_dict['Reachability'] != 0 and down is True:
                send_mail(msg = 'Host %s Critical alarm: CLEARED \n\n Host %s (%s) \n UP Time: %s' \
                          %(self.name, self.name, self.host, ctime(host_dict['Time'])))
                down_nr = 0
                down = False
                inform = False

            sleep(self.inter - self.pkt_count * self.pkt_inter)
        
        run = sql().get_value(db = self.read_db, tb = self.read_tb, field = 'Monitoring',
                              value = self.host, lookup = 'IP')

        self.stop()

    def stop(self):

        self._Thread__stop()
