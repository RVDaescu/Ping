from re import *
import pexpect

def ping(host, count = 10):
    child = pexpect.spawn('ping -c %d %s' %(count, host))
    output = []
    while 1:
        line = child.readline()
	output.append(line)
	if not line: break
        
    output = ''.join(output)

    search =  output.split(',')

    for j in search:
        if 'packet loss' in j:
            pl = j.split(' ')
            pl = pl[1]

    print '%s: %s packet loss\n' %(host, pl),
