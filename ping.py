from re import *
import pexpect

def ping(host, count = 10):
    child = pexpect.spawn('ping -i 1 -c %d %s' %(count, host))
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

    print '%s: %s packet loss\n' %(host, pl),
