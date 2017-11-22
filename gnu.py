
import numpy
import Gnuplot


def rainfall_intensity_t10(t): 
    return 11.23 * (t**(-0.713))

def rainfall_intensity_t50(t): 
    return 18.06 * (t**(-0.713))

g = Gnuplot.Gnuplot()
g.title("rainfall intensity")

g.xlabel("t (min)")
g.ylabel("i (mm/min)")

g("set grid")
g("set xtic 10")
g("set ytic 1")

x = numpy.arange (start=2, stop=120, step=0.5, dtype='float_')

y1 = rainfall_intensity_t10(x) # yields another numpy.arange object
y2 = rainfall_intensity_t50(x) # ...

d1 = Gnuplot.Data (x, y1, title="intensity i (T=10)", with_="lines")
d2 = Gnuplot.Data (x, y2, title="intensity i (T=50)", with_="lines")

g("set terminal svg")
g.plot(d1, d2) # write SVG data directly to stdout ...

g.hardcopy (filename='/tmp/rainfall-intensity.png', terminal='png') # write last plot to another terminal
g.hardcopy (filename='/tmp/rainfall-intensity.svg', terminal='svg') # ...

del g
