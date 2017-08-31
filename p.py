from snf import *

f = open('192.168.1.228.txt', 'w')

tm = 100

while tm > 0:
    f.write(str(main('192.168.1.228', count = 10, inter = 0.01)))
    f.write('\n')
    tm-=10
    sleep(10)
    
f.close()
