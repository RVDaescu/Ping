from time import sleep, ctime, time
from traffic import *
from sql_lib import *
from mail import *

def host(host, db_name, pkt_count = 3, pkt_inter = 1, interval = 10, repeat_nr = 100, 
         loop = False, minor_alarm = None):
    
    down = False
    lnk_dgr = False

    for i in range(repeat_nr):
        
        print 'Starging %s: %r' %(i, time())

        host_dict = {}
        table = 'table_%s' %host.replace('.', '_')

        host_data = main(host, count = pkt_count, inter = pkt_inter, out_dict = host_dict)

        host_data.start()
        host_data.join()
 
        if minor_alarm:
            if host_dict['Reachability'] < minor_alarm and lnk_dgr is False:
                send_mail(msg = 'Host %s Minor alarm: Link degradation \n\n Host %s \n Time: %s \n Reachability: %r' %(host, host, ctime(host_dict['Time']), host_dict['Reachability'] ))
                lnk_dgr = True
            
            elif  host_dict['Reachability'] < minor_alarm and lnk_dgr is True:
                pass

            elif host_dict['Reachability'] > minor_alarm and lnk_dgr is True:
                lnk_dgr = False


        if host_dict['Reachability'] == 0 and down is False:
            send_mail(msg = 'Host %s Critical alarm: DOWN \n\n Host %s \n Down Time: %s' %(host, host, ctime(host_dict['Time'])))
            down = True
        
        elif host_dict['Reachability'] == 0 and down is True:
            pass

        elif host_dict['Reachability'] != 0 and down is True:
            send_mail(msg = 'Host %s Critical alarm: CLEARED \n\n Host %s \n UP Time: %s' %(host, host, ctime(host_dict['Time'])))
            down = False

        sql_add_value(db_name = db_name, tb_name = table, **host_dict)

        sleep(interval)
        print 'Ending %s: %r' %(i, time())

