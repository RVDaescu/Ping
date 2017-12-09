from utils import time_con
from sql_lib import sql
from time import ctime,time
import Gnuplot, os

def plot_to_file(db, tb, field = 'Reachability', start = None, end = None):

    data = sql().get_data(db = db,tb = tb, field = 'Time,'+field, start = start, end = end)

    type = {'Reachability': '(%)',
            'Jitter': '(ms)',
            'Avg_Rsp_time': '(ms)'}

    host = tb.replace('_','.')[3:]

    header = data.pop(0)

    g = Gnuplot.Gnuplot()
    g('set terminal png size 1980,1080')
    g.title("Host %s" %host)

    g.xlabel("Time")
    g.ylabel("%s %s" %(field.replace('_',' '), type[field]))
   
    tm_ls = [i[header['Time']] for i in data]
    xtic = int(max(tm_ls)-min(tm_ls))/4

    data_list = [i[header[field]] for i in data]
    rc = Gnuplot.Data(tm_ls, data_list, title = field.replace('_',' '), with_='lines')

    g("set grid")
    #g('set xtic auto')
    g('set xtics ("%s" %s, "%s" %s, "%s" %s, "%s" %s, "%s" %s)' \
                %(time_con(tm = tm_ls[10]), tm_ls[10],
                  time_con(tm = tm_ls[len(tm_ls)/4]), tm_ls[len(tm_ls)/4],
                  time_con(tm = tm_ls[len(tm_ls)/2]), tm_ls[len(tm_ls)/2],
                  time_con(tm = tm_ls[len(tm_ls)*3/4]), tm_ls[len(tm_ls)*3/4],
                  time_con(tm = tm_ls[-1]), tm_ls[-1]))
    if 'Reachability' == field:
        g('set ytics 0,10,100')
    elif field in ['Jitter','Avg_Rsp_time']:
        mx = max(data_list)*1.5
        g('set ytic auto')

    g("set terminal svg")
    g.plot(rc) # write SVG data directly to stdout ...

    name = host + '_' + ctime(time())

    cwd = os.getcwd()

    g.hardcopy (filename='%s/graphs/%s.png' %(cwd,name), terminal='png') # write last plot to another terminal

    del g
