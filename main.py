import threading
from threading import Thread

from time import time, sleep, ctime
from traffic import *
from sql_lib import *
from mail import *
#import sys

#sys.dont_write_bytecode = True

class monitor(Thread):

    def __init__(self, host, db, pkt_count = 3, pkt_inter = 1, 
                 inter = 300, name = None, debug = False, link_dgr = None):
    
        Thread.__init__(self)

        self.host = host            #IP to interogate
        self.pkt_count = pkt_count  #number of packets per interogation
        self.pkt_inter = pkt_inter  #number of seconds between packets
        self.inter = inter          #number of seconds between iterations
        self.name = name            #NS or name of host
        self.db = db                #SQL db to write data in; table will take host ip
        #print specific info
        self.debug = debug 
        self.link_dgr = link_dgr    #min percentage on which to notify the user on the packet loss; if 'None' it's not ran
        self.work = True


    def run(self):
        
        Thread.run(self)
        
        down = False
        dgr = False
        down_nr = 0
        dgr_nr = 0

        if self.inter <= (self.pkt_count * self.pkt_inter)+2:
            print 'Interval between polls is smaller than the duration of the poll'
            return False

        while self.work:
            
            run_start = time.time()

            host_dict = {}
            host_data = traffic(host = self.host, count = self.pkt_count, 
                                inter = self.pkt_inter, debug = self.debug, 
                                out_dict = host_dict)

            host_data.start()
            host_data.join()
            
            table = self.name.replace('.','_')

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
                    send_mail(subj = 'Host %s Critical alarm' %self.name,  
                            msg = 'Alarm DOWN \n Host %s (%s) \n Down since: %s' \
                                 %(self.name, self.host, ctime(host_dict['Time'])))
                    down = True

            elif host_dict['Reachability'] != 0 and down is True:
                send_mail(subj = 'Host %s Critical alarm' %self.name,
                        msg = 'Alarm CLEARED \n Host %s (%s) \n UP since: %s' \
                          %(self.name, self.host, ctime(host_dict['Time'])))
                down_nr = 0
                down = False

            if run_start + self.inter > time.time():
                sleep(run_start + self.inter - time.time())
        
        self.stop()

    def stop(self):

        self._Thread__stop()
