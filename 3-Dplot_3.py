from numpy import *
import pylab as p

import mpl_toolkits.mplot3d.axes3d as p3
C = p3.mplot3d.contourf(X, Y, Z, *args, **kwargs)
levels, colls = (C.levels, C.collections)


delta = 0.025
x = arange(-3.0, 3.0, delta)
y = arange(-2.0, 2.0, delta)
X, Y = p.meshgrid(x, y)
Z1 = p.bivariate_normal(X, Y, 1.0, 1.0, 0.0, 0.0)
Z2 = p.bivariate_normal(X, Y, 1.5, 0.5, 1, 1)
#
Z = 10.0 * (Z2 - Z1)
fig = p.figure()
ax = p3.Axes3D(fig)
ax.contour3D(X,Y,Z)
ax.plot_wireframe(X,Y,Z)
ax.set_xlabel( 'X' )
ax.set_ylabel( 'Y' )
ax.set_zlabel( 'Z' )
#fig.add_axes(ax)
p.show()
