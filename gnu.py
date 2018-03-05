from utils import time_con, list_split, time_epoch
from sql_lib import sql
from time import ctime,time
import Gnuplot, os
import sys

sys.dont_write_bytecode = True


def plot_to_file(db, tb, field = 'Latency', start = None, end = None, mode = 'average'):
    """
    method for plotting data from sql file (db,tb) with a certain mode 
    start/end = shhould be in format dd/mm/yy-HH:MM:SS
    average - divides the list in 100 smaller lists and for each division
              makes its average
    max - divides the list in 100 smaller lists and for each division
              returns the max value
    min - divides the list in 100 smaller lists and for each division
              returns the min value
    fractile(x) - divides the list in 100 smaller lists and for each division
              returns the x% fractile (default should be 49%)
    """

    start = time_epoch(tm = start) if start else None
    end = time_epoch(tm =end) if end else None

    #read data from the sql file
    data = sql().get_data(db = db,tb = tb, field = 'Time,'+field, 
                          start = start, end = end)

    type = {'Reachability': '(%)',
            'Jitter': '(ms)',
            'Latency': '(ms)',
            'Pkt_loss': '(%)'}

    #get the ip of the host and set is as a name
    host = tb.replace('_','.')[3:]

    header = data.pop(0)

    #initiate gnuplot 
    g = Gnuplot.Gnuplot()
    g('set terminal png size 1280,960')
    #give graphic a title name
    g.title("Host %s" %host)

    g('set datafile missing "?"')

    g.xlabel("Time")
    g.ylabel("%s %s" %(field.replace('_',' '), type[field]))
   
    time_ls = [i[header['Time']] for i in data]
    time_ls = list_split(list = time_ls, mode = 'average')

    

    data_list = [i[header[field]] for i in data]
    data_list = list_split(list = data_list, mode = mode)
    
    rc = Gnuplot.Data(time_ls, data_list, title = field.replace('_',' '), with_ = 'line')

#    if (len(time_ls) or len(data_list)) <= 5:
#        print 'Lists are to small'
#        return False

    g("set grid back")
    g('set xtics ("%s" %s, "%s" %s, "%s" %s, "%s" %s, "%s" %s)' \
                %(time_con(tm = time_ls[0]), time_ls[1],
                  time_con(tm = time_ls[len(time_ls)/4]), time_ls[len(time_ls)/4],
                  time_con(tm = time_ls[len(time_ls)/2]), time_ls[len(time_ls)/2],
                  time_con(tm = time_ls[len(time_ls)*3/4]), time_ls[len(time_ls)*3/4],
                  time_con(tm = time_ls[-1]), time_ls[-1]))
    
    if 'Reachability' == field:
        g('set ytics (0,25,50,75,100)')
        g('set yrange [0:105]')
    elif field in ['Jitter','Latency']:
        g('set ytic auto')
        g('set yrange auto')
    
    g("set terminal svg")
    g.plot(rc) # write SVG data directly to stdout ...

    name = host + '_'+ mode +'_' + field + '_' + ctime(time())

    cwd = os.getcwd()

    g.hardcopy (filename='%s/graphs/%s.png' %(cwd,name), terminal='png') # write last plot to another terminal
    del g
