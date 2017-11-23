from sql_lib import sql
import Gnuplot

def plot_to_file(db_name, tb_name, fields = '*')

    db = sql()
    data = db.get_data(db_name = db_name,tb_name= tb_name, field = fields)

    host = tb.replace('_','.')[3:]

    g = Gnuplot.Gnuplot()
    g.title("Host %s",%host)

    g.xlabel("Time")
    g.ylabel("Reachability (%)")

    time_list = [i[1] for i in data]
    reach_list = [i[0] for i in data]

    xtic = int(max(time_list)-min(time_list))/25

    g("set grid")
    g("set xtic %s" %xtic)
    g("set ytic 10")


    d = Gnuplot.Data (time_list, reach_list, title="Reachability", with_="lines")

    g("set terminal svg")
#    g.plot(d) # write SVG data directly to stdout ...

    g.hardcopy (filename='/home/radu/Ping/graphs/%s.png', terminal='png') # write last plot to another terminal

    del g
