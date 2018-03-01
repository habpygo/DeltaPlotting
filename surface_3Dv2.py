from datetime import datetime
import matplotlib as mplt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


X = []
Y = []
Z = []
#  0     1    2    3    4     5   6  7   8
# Year Month Day Hour Minute Open Hi Lo Close

for line in open('euro-15minute.txt'): # values separated by tabs ('\t')
    datum = datetime(int(line.split('\t')[0]), int(line.split('\t')[1]), int(line.split('\t')[2]))
    x_num = mplt.dates.date2num(datum)
    #X.append(mplt.dates.date2num(datum))
    X.append(x_num)
    time = datetime(int(line.split('\t')[0]), int(line.split('\t')[1]),
                    int(line.split('\t')[2]), int(line.split('\t')[3]), int(line.split('\t')[4]))
    y_num = mplt.dates.date2num(time)
    #Y.append(mplt.dates.date2num(time))
    Y.append(y_num - x_num)
    Close = float(line.split()[8].strip('\n'))
    Z.append(Close)
    #print("Datum ", datum, x_num, "Tijd ", time, y_num)
X = np.asarray(X)
Y = np.asarray(Y)
Z = np.asarray(Z)


start_Red_day = datetime(2012, 3, 1) 
start_Blue_day = datetime(2012, 3, 2) # 1 maart 2012 was een Rood jaar
start_Orange_day = datetime(2012, 3, 3) # 2012 was een schrikkeljaar; 2016 ook
start_Green_day = datetime(2012, 3, 4)

## for debugging purposes ##
# printing out and checking the values
#for z in Z:
#    print(z)

#print("Z-Shape is ", Z.shape, "X-Shape is ", X.shape, "and Y-Shape is ", Y.shape)
## no data problems
# checking if lists are equal
#print("Length X is ", len(X),"length Y is ", len(Y),"length Z is ", len(Z))
#print("Shape X is ", X.shape,"Shape Y is ", Y.shape,"Shape Z is ", Z.shape)

## PLOT THE FIGURE
plt.close('all')

#fig = plt.figure()
#fig, ax = plt.subplots()
ax = plt.subplot(111, projection='3d') 

ax.set_xlabel( 'Day' )
ax.set_ylabel( 'Time' )
ax.set_zlabel( 'Close' )

ax.plot_wireframe(X, Y, Z, label='Data from July 2012')
ax.legend()

plt.show()

