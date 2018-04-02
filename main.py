import threading
from threading import Thread

from time import sleep, ctime
from traffic import *
from sql_lib import *
from mail import *
import sys

sys.dont_write_bytecode = True


class monitor(Thread):

    def __init__(self, host, db, read_db, read_tb, debug = False, link_dgr = None):
    
        Thread.__init__(self)

        self.host = host            #IP to interogate
        self.db = db                #SQL db to write data in; table will take host ip
        self.read_db = read_db      #sql db where monitoring status for IP is found
        self.read_tb = read_tb      #sql table where IP is found
       
        #print specific info
        self.debug = debug 

        self.link_dgr = link_dgr    #min percentage on which to notify the user on the packet loss; if 'None' it's not ran

    def reinit(self):
        """
        Method neccessary for having at each iteration the latest info on the host
        """

        host_info = sql().get_row(db = self.read_db, tb = self.read_tb, lookup = self.host)
        self.pkt_count = host_info[1][host_info[0]['pkt_count']]
        self.pkt_inter =  host_info[1][host_info[0]['pkt_inter']]
        self.inter = host_info[1][host_info[0]['interval']]
        self.name = ip_to_name(db = self.read_db, tb = self.read_tb, ip = self.host)     #name or NS of IP/host

    def run(self):
        
        Thread.run(self)
        
        down = False
        dgr = False
        down_nr = 0
        dgr_nr = 0

        self.reinit()

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
                if host_dict['Pkt_loss'] >= self.link_dgr and dgr is False:
                    dgr_nr += 1
                    #after 5 consecutive degradations, send an email
                    if dgr_nr == 5:
                        send_mail(subj = 'Host %s Minor alarm: Link degradation' %self.name, 
                                  msg = 'Host %s (%s) \n Time: %s \n Pkt_loss: %r'\
                                  %(self.name, self.host, ctime(host_dict['Time']), host_dict['Pkt_loss']))
                        dgr = True

                elif host_dict['Reachability'] < self.link_dgr and dgr is True:
                    link_dgr = False
                    dgr_nr = 0

            if host_dict['Reachability'] == 0 and down is False:
                down_nr += 1
                if down_nr == 3:
                        send_mail(subj = 'Host %s Critical alarm: DOWN' %self.name,  
                                  msg = 'Host %s (%s) \n Down Time: %s' \
                                  %(self.name, self.host, ctime(host_dict['Time'])))
                        down = True

            elif host_dict['Reachability'] != 0 and down is True:
                send_mail(subj = 'Host %s Critical alarm: CLEARED' %self.name,
                          msg = 'Host %s (%s) \n UP Time: %s' \
                          %(self.name, self.host, ctime(host_dict['Time'])))
                down_nr = 0
                down = False

            sleep(self.inter - self.pkt_count * self.pkt_inter)
        
        run = sql().get_value(db = self.read_db, tb = self.read_tb, field = 'Monitoring',
                              value = self.host, lookup = 'IP')

        self.stop()

    def stop(self):

        self._Thread__stop()
