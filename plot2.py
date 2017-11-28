import numpy
import Gnuplot
from random import sample

g = Gnuplot.Gnuplot()
g.title("rainfall intensity")

g.xlabel("t (min)")
g.ylabel("Y1 (%)")
g.ylabel("Y2 (ms)")

g("set grid")
g("set xtic 10")
g("set ytic 0,10,100")
g("set y2tic 0,5,30")

x = [i for i in range(0,10)]

y1 = sample(range(1,30),10)
y2 = sample(range(80,100),10)

d1 = Gnuplot.Data (x, y1, title="Y1", with_="lines")
d2 = Gnuplot.Data (x, y2, title="Y2", with_="lines")

g("set terminal svg")
g.plot(d1, d2) # write SVG data directly to stdout ...

g.hardcopy (filename='/home/radu/Ping/graphs/plot.png', terminal='png') # write last plot to another terminal
#g.hardcopy (filename='/tmp/rainfall-intensity.svg', terminal='svg') # ...

del g
