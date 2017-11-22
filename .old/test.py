from ping import ping
import threading

def test(list):

    ip = open(list, 'r')

    ip_list =ip.readlines()

    threads = []

    for i in range(len(ip_list)):
        t = threading.Thread(target = ping, args = (ip_list[i].replace('\n',''), ), kwargs = {'mode': 'qos'})
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
