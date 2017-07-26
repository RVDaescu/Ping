import pexpect

def ping(host):
    child = pexpect.spawn('ping -c 5 %s' %host)
    output = []
    while 1:
        line = child.readline()
		output.append(line)
		if not line: break

    ok = ', 0% packet loss'
        
    output = ''.join(output)

    if ok not in output:
        print 'ICMP test failed for %s\n' %host,
    else:
        print 'Host %s has no packet loss\n' %host,
