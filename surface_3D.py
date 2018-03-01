from datetime import datetime
import matplotlib as mplt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter


X = []
Y = []
Z = []
#  0     1    2    3    4     5   6  7   8
# Year Month Day Hour Minute Open Hi Lo Close

for line in open('from_sep_2015.txt'): # values separated by tabs ('\t')
    datum = datetime(int(line.split('\t')[0]), int(line.split('\t')[1]), int(line.split('\t')[2]))
    X.append(mplt.dates.date2num(datum))
    time = datetime(int(line.split('\t')[0]), int(line.split('\t')[1]),
                    int(line.split('\t')[2]), int(line.split('\t')[3]), int(line.split('\t')[4]))
    Y.append(mplt.dates.date2num(time))
    Z.append(float(line.split()[8].strip('\n')))

#X = np.asarray(X)
#Y = np.asarray(Y)
Z = np.asarray(Z)

## for debugging purposes ##
# printing out and checking the values
for z in Z:
    print(z)

#print("Z-Shape is ", Z.shape, "X-Shape is ", X.shape, "and Y-Shape is ", Y.shape)
## no data problems
# checking if lists are equal
print(len(X), len(Y), len(Z))

fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.arange(0, 1022, 1)
Y = np.arange(0, 1022, 1)
#R = np.sqrt(X**2 + Y**2)
#Z = np.sin(R)

print("Z-Shape is ", Z.shape, "X-Shape is ", X.shape, "and Y-Shape is ", Y.shape)
## no data problems
X, Y = np.meshgrid(X, Y)
surf = ax.plot_surface(X, Y, Z, rstride=10, cstride=10, cmap=cm.coolwarm, linewidth=0, antialiased=False)

#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

"""
fig = plt.figure()
ax = fig.add.subplot(111, projection='3d') # <= problem?
X = np.arange(0, 1022, 1)
Y = np.arange(0, 1022, 1)

ax.set_xlabel( 'Day' )
ax.set_ylabel( 'Time' )
ax.set_zlabel( 'Close' )

ax.plot_wireframe(X, Y, Z, label='2015 date range')
ax.legend()

plt.show()

# no error mesages here; example plots correctly
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X = [11, 11, 11, 11, 11, 11]
Y = [1,2,3,4,5,6] 
Z = [1.09772, 1.09955, 1.09882, 1.09935, 1.09992, 1.09941]

ax.set_xlabel( 'Day' )
ax.set_ylabel( 'Minute' )
ax.set_zlabel( 'Close' )

ax.plot_wireframe(X, Y, Z, label='2015 data range')
ax.legend()

plt.show()



fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_zlim(-1.01, 1.01)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)

"""
