from re import *
import pexpect
import time

def ping(host, count = 50):
    start = time.time() 
    child = pexpect.spawn('ping -i 1 -c %d %s' %(count, host))
    child.timeout = 300
    output = []
    while 1:
        line = child.readline()
	output.append(line)
	if not line: break
        
    output = ''.join(output)

    src =  output.split(',')

    for j in src:
        if 'packet loss' in j:
            pl = j.split(' ')
            pl = pl[1]

    end = time.time() - start 

    print '[%.2f s] - %s: %s packet loss\n' %(end, host, pl),
