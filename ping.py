import pexpect
from re import search
import time

def ping(host, mode = 'ping'):
    """
    Descr:
    - mode: ping - reachability test
            qos - response time, jitter
                  interval is 0.1 and count = 1000
                  """
    res_dict = {}
    if mode == 'ping':
        string = 'ping -c 10 -i 1 %s' %host
    elif mode == 'qos':
        string = 'ping -c 50 -i 0.2 %s' %host

    start = time.time() 
    child = pexpect.spawn(string)
    child.timeout = 300
    output = []
   
    while 1:
        line = child.readline()
	output.append(line)
	if not line: break
   
    end = time.time() - start      
   
    output = ''.join(output)

    src =  output.split(',')
   
    for j in src:
        if 'packet loss' in j:
            pl = j.split(' ')
            res_dict['pkt_loss'] = pl[1]
    
    if '100%' in res_dict['pkt_loss'] and mode == 'qos':
        print '%s is down - cannot obtaind response times or jitter' %host
        return False
    
    elif '100%' in res_dict['pkt_loss'] and mode == 'ping':
        print '[%.2f s] - %s: %s packet loss\n' %(end, host, res_dict['pkt_loss']),
        return False
    elif mode == 'ping':
        print '[%.2f s] - %s: %s packet loss\n' %(end, host, res_dict['pkt_loss']),
        return True
    else:
        res = search('min/avg/max/mdev.*ms', output).group().split(' ')
        avg_rsp = float(res[-2].split('/')[1])
        res_dict['avg_rsp'] = avg_rsp
        
        jitter = float(res[-2].split('/')[-1])
        res_dict['jitter'] = jitter
        
        print '[%.2f s] - %s: Average response time is %r and jitter is %r' %(end, host, res_dict['avg_rsp'], res_dict['jitter'])

        return res_dict
