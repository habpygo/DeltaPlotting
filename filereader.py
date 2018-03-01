from datetime import datetime
from datetime import timedelta
import matplotlib as mplt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import heapq


Red_X = [] ; Red_Y = [] ; Red_Z = [] ; Blue_X = [] ; Blue_Y = [] ; Blue_Z = []
Orange_X = [] ; Orange_Y = [] ;Orange_Z = [] ; Green_X = [] ; Green_Y = [] ; Green_Z = []

start_Red_day = datetime(2012, 3, 1)
start_Blue_day = datetime(2012, 3, 2) # 1 maart 2012 was een Rood jaar
start_Orange_day = datetime(2012, 3, 3) # 2012 was een schrikkeljaar; 2016 ook
start_Green_day = datetime(2012, 3, 4)

def kleur_bepaler(datum):
    result = (datum - start_Red_day).total_seconds()
    if result % 345600 == 0:
        #print("Voor datum" , datum, "The result was Red")
        return "Red"
    result = (datum - start_Blue_day).total_seconds()
    if result % 345600 == 0:
        #print("Voor datum ", datum, "The result was Blue")
        return "Blue"
    result = (datum - start_Orange_day).total_seconds()
    if result % 345600 == 0:
        #print("Voor datum ", datum, "The result was Orange")
        return "Orange"
    result = (datum - start_Green_day).total_seconds()
    if result % 345600 == 0:
        #print("Voor datum ", datum, "The result was Green")
        return "Green"

#  0     1    2    3    4     5   6  7   8
# Year Month Day Hour Minute Open Hi Lo Close

for line in open('test.txt'): # values separated by tabs ('\t') test.txt
    datum = datetime(int(line.split('\t')[0]), int(line.split('\t')[1]), int(line.split('\t')[2]))
    x_num = mplt.dates.date2num(datum)
    time = datetime(int(line.split('\t')[0]), int(line.split('\t')[1]), int(line.split('\t')[2]), int(line.split('\t')[3]), int(line.split('\t')[4]))
    y_num = mplt.dates.date2num(time)
    Close = float(line.split()[8].strip('\n'))
    if kleur_bepaler(datum) == "Red": # replace datum with x_num etc.
        #print("Red kleur gevonden")
        Red_X.append(x_num)
        Red_Y.append(y_num - x_num)
        Red_Z.append(Close)
    elif kleur_bepaler(datum) == "Blue":
        #print("Blue kleur gevonden")
        Blue_X.append(x_num)
        Blue_Y.append(y_num - x_num)
        Blue_Z.append(Close)
    elif kleur_bepaler(datum) == "Orange":
        #print("Orange kleur gevonden")
        Orange_X.append(x_num)
        Orange_Y.append(y_num - x_num)
        Orange_Z.append(Close)
    else:
        #print("Green kleur gevonden")
        Green_X.append(x_num)
        Green_Y.append(y_num - x_num)
        Green_Z.append(Close)

## FIND THE HI's AND LO's






## PLOT THE FIGURE
plt.close('all') # clean up memory

#fig = plt.figure()
#fig, ax = plt.subplots()
ax = plt.subplot(111, projection='3d')

ax.set_xlabel( 'Day' )
ax.set_ylabel( 'Time' )
ax.set_zlabel( 'Close' )

#ax.plot_wireframe(Green_X, Green_Y, Green_Z, label='Green - Data from test.txt 2015')
ax.plot_wireframe(Red_X, Red_Y, Red_Z, label='Red - Data from test.txt 2015')
#ax.plot_wireframe(Blue_X, Blue_Y, Blue_Z, label='Blue - Data from test.txt 2015')
#ax.plot_wireframe(Orange_X, Orange_Y, Orange_Z, label='Orange - Data from test.txt 2015')
ax.legend()

plt.show()

