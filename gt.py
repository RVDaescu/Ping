from gnu import *
from time import sleep

for f in ['Reachability','Jitter','Avg_Rsp_time']:
    plot_to_file(db = 'host_gns.sqlite',tb = 'tb_10_10_107_2',field = f)
    sleep(1)
