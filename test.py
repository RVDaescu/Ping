from ping import ping
import threading

ip = open('ip3.txt', 'r')

ip_list = []

ip_list.append(ip.readlines())
ip_list = ip_list[0]

#for i in range(len(ip_list)):
#    print ip_list[i].replace('\r\n','')

threads = []

for i in range(len(ip_list)):
    t = threading.Thread(target = ping, args = (ip_list[i].replace('\r\n',''),))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

