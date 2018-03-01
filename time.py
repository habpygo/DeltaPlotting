import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import datetime as datetime

# Make a series of events 1 day apart
x = mpl.dates.drange(datetime.datetime(2009,10,1),
                     datetime.datetime(2010,1,15),
                     datetime.timedelta(days=1))
# Vary the datetimes so that they occur at random times
# Remember, 1.0 is equivalent to 1 day in this case...
x += np.random.random(x.size)

# We can extract the time by using a modulo 1, and adding an arbitrary base date
times = x % 1 + int(x[0]) # (The int is so the y-axis starts at midnight...)

# I'm just plotting points here, but you could just as easily use a bar.
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot_date(x, times, 'ro')
ax.yaxis_date()
fig.autofmt_xdate()

plt.show()

# First convert to pandas Period
period = pandas.tseries.period.Period(ordinal=int(d1), freq=ax.freq)
# Then convert to pandas timestamp
ts = period.to_timestamp()
# Then convert to date object
dt = ts.to_datetime()
