from utils import time_con, list_split, time_epoch
from sql_lib import sql
from time import ctime,time
from datetime import datetime as dt
import matplotlib.pyplot as plt
import sys, os

sys.dont_write_bytecode = True


def plot(db, tb, reach = True, pkt_loss = True, jitter = True, latency = True,
         start = None, end = None, mode = 'average', name = False):
    """
    method for plotting data from sql file (db,tb) with a certain mode:
    average - divides the list in 100 smaller lists and for each division
              makes its average
    max - divides the list in 100 smaller lists and for each division
              returns the max value
    min - divides the list in 100 smaller lists and for each division
              returns the min value
    fractile_x - divides the list in 100 smaller lists and for each division
              returns the x% fractile (default should be 49%)
    start/end = should be in format dd/mm/yy-HH:MM:SS
    name = name to give to file
    """

    reach = ',Reachability' if reach else ''
    pkt_loss = ',Pkt_loss' if pkt_loss else ''
    jitter = ',Jitter' if jitter else ''
    #latency = ',Latency' if latency else ''
    latency = ',Avg_Rsp_time' if latency else ''

    start = time_epoch(tm = start) if start else None
    end = time_epoch(tm =end) if end else None

    data_get = 'Time%s%s%s%s' %(reach, pkt_loss, jitter, latency)

    #read data from the sql file
    data = sql().get_data(db = db,tb = tb, field = data_get, 
                          start = start, end = end)

    #get the name of the host and set is as a name
    host = '.'.join(tb.split('_')[1:])

    header = data.pop(0)
    
    #proccess data
    time_list = [i[header['Time']] for i in data]
    if mode is not None:
        time_list= list_split(list = time_list, mode = 'average')
    time_list = [dt.fromtimestamp(i) for i in time_list]

    if reach:
        reach_list = [i[header[reach.lstrip(',')]] for i in data]
        reach_list = list_split(list = reach_list, mode = mode)
    if pkt_loss:
        pkt_loss_list = [i[header[pkt_loss.lstrip(',')]] for i in data]
        pkt_loss_list = list_split(list = pkt_loss_list, mode = mode)
    if jitter:
        jitter_list = [i[header[jitter.lstrip(',')]] for i in data]
        jitter_list = list_split(list = jitter_list, mode = mode)
    
    if latency:
        latency_list = [i[header[latency.lstrip(',')]] for i in data]
        latency_list = list_split(list = latency_list, mode = mode)
 
    fig, ax1 = plt.subplots()

    plt.setp(ax1.get_xticklabels(), rotation=45)

    #plotting reach and jitter in percents with axis on left side
    #    and jitter/latency with miliseconds on right side
    
    if reach:
        r = ax1.plot(time_list, reach_list, 'g', label = 'Reachability')
    if pkt_loss:
        p = ax1.plot(time_list, pkt_loss_list, 'r', label = 'Packet Loss')

    ax1.set_yticks([i for i in range(0,101,10)])
    ax1.set_xlim([time_list[0], time_list[-1]])
    ax1.set_xlabel('Time')
    ax1.minorticks_on()

    # Make the y-axis label, ticks and tick labels match the line color.
    if reach and pkt_loss:
        ax1.set_ylabel('Reachabilty/Packet loss (%)')
    elif reach and not pkt_loss:
        ax1.set_ylabel('Reachabilty (%)')
    elif not reach and pkt_loss:
        ax1.set_ylabel('Packet loss (%)')

    ax2 = ax1.twinx()

    if latency:
        l = ax2.plot(time_list, latency_list, 'y', label = 'Latency')
    if jitter:
        j = ax2.plot(time_list, jitter_list, 'm', label = 'Jitter')
    
    if jitter and latency:
        ax2.set_ylabel('Jitter/Latency (ms)')
    elif jitter and not latency:
        ax2.set_ylabel('Jitter (ms)')
    elif not jitter and latency:
        ax2.set_ylabel('Latency (ms)')
 
    legend = []

    if reach:
        legend = legend + r
    if pkt_loss:
        legend = legend + p
    if jitter:
        legend = legend + j
    if latency:
        legend = legend + l

    ax2.minorticks_on()
    ax2.legend(bbox_to_anchor=(0.1, -0.1), handles = legend)
    ax2.tick_params(axis = 'y', which = 'minor', bottom = 'off')
    ax2.set_xlim([time_list[0], time_list[-1]])

    cwd = os.getcwd()

    if not name:
        name = cwd + '/graphs/' + host + '_' + ctime(time()) + '.png'
 
    fig.tight_layout()
    plt.savefig(name, dpi = 250, papertype = 'A4', bbox_inches='tight')
    plt.show()
