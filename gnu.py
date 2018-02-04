from utils import time_con, list_split
from sql_lib import sql
from time import ctime,time
import Gnuplot, os

def plot_to_file(db, tb, field = 'Avg_Rsp_time', start = None, end = None, mode = 'average'):

    data = sql().get_data(db = db,tb = tb, field = 'Time,'+field, start = start, end = end)

    type = {'Reachability': '(%)',
            'Jitter': '(ms)',
            'Avg_Rsp_time': '(ms)'}

    host = tb.replace('_','.')[3:]

    header = data.pop(0)

    g = Gnuplot.Gnuplot()
    g('set terminal png size 1280,960')
    g.title("Host %s" %host)

    g.xlabel("Time")
    g.ylabel("%s %s" %(field.replace('_',' '), type[field]))
   
    tm_ls = [i[header['Time']] for i in data]
    tm_ls = list_split(list = tm_ls, mode = mode)

    data_list = [i[header[field]] for i in data]
    data_list = list_split(list = data_list, mode = mode)
    
    rc = Gnuplot.Data(tm_ls, data_list, title = field.replace('_',' '), with_ = 'histeps')

    g("set grid back")
    g('set xtics ("%s" %s, "%s" %s, "%s" %s, "%s" %s, "%s" %s)' \
                %(time_con(tm = tm_ls[0]), tm_ls[1],
                  time_con(tm = tm_ls[len(tm_ls)/4]), tm_ls[len(tm_ls)/4],
                  time_con(tm = tm_ls[len(tm_ls)/2]), tm_ls[len(tm_ls)/2],
                  time_con(tm = tm_ls[len(tm_ls)*3/4]), tm_ls[len(tm_ls)*3/4],
                  time_con(tm = tm_ls[-1]), tm_ls[-1]))
    
    if 'Reachability' == field:
        g('set ytics (0,25,50,75,100)')
        g('set yrange [0:105]')
    elif field in ['Jitter','Avg_Rsp_time']:
        g('set ytic auto')
        g('set yrange auto')
    g("set terminal svg")
    g.plot(rc) # write SVG data directly to stdout ...

    name = host + '_'+ mode +'_' + ctime(time())

    cwd = os.getcwd()

    g.hardcopy (filename='%s/graphs/%s.png' %(cwd,name), terminal='png') # write last plot to another terminal
    print name
    del g
