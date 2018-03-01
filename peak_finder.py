#!/anaconda/bin/python

import numpy as np
from numpy import NaN, Inf, arange, isscalar, asarray, array


def peakdet(v, delta, x = None):
    """
    Converted from MATLAB script at http://billauer.co.il/peakdet.html

    Returns two arrays

    function [maxtab, mintab]=peakdet(v, delta, x)
    %PEAKDET Detect peaks in a vector
    %        [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local
    %        maxima and minima ("peaks") in the vector V.
    %        MAXTAB and MINTAB consists of two columns. Column 1
    %        contains indices in V, and column 2 the found values.
    %
    %        With [MAXTAB, MINTAB] = PEAKDET(V, DELTA, X) the indices
    %        in MAXTAB and MINTAB are replaced with the corresponding
    %        X-values.
    %
    %        A point is considered a maximum peak if it has the maximal
    %        value, and was preceded (to the left) by a value lower by
    %        DELTA.

    """

    maxtab = []
    mintab = []

    if x is None:
        x = arange(len(v))

    v = asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = Inf, -Inf #mn wordt + oneindig, mx wordt - oneindig
    mnpos, mxpos = NaN, NaN

    lookformax = True

    for i in arange(len(v)):
        this = v[i]
        if this > mx: #eerste ronde is altijd True
            mx = this #van - oneindig tot eerste waarde
            mxpos = x[i] # x is de array van i tot len(v); dus mxpos = x[1]
        if this < mn: # niet waar dus wordt eerste keer overgeslagen
            mn = this
            mnpos = x[i]

        if lookformax: #eerste ronde altijd waar
            if this < mx*(1 - (0.75 * delta)): # if this < mx-delta
                maxtab.append((mxpos, mx)) #wordt alleen gedaan als this < mx...
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn*(1 + delta):
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    maxtab = array(maxtab); mintab = array(mintab)

    return maxtab, mintab

x = [ 3, 5, 6, 3, 12, 14, 15, 16, 17, 10, 9, 8, 7, 20, 21, 22, 23, 12, 10, 16, 19, 30, 31, 32, 40,
     32]
x2 = [ 6, 5, 4, 3, 12, 14, 15, 16, 17, 10, 9, 8, 7, 20, 21, 22, 23, 12, 10, 16, 19, 30, 31, 32, 40,
     32]

[X_max,X_min] = peakdet(x, 0.002)
XY = np.concatenate((X_max,X_min), axis=0)
XY_sorted = XY[np.argsort(XY[:, 0])]

print(X_max)
print("X_min is: ")
print(X_min)
print("Totale array is: ")
print(XY)
print("The sorted array is ")
print(XY_sorted)
XY_return = []

#algoritme verzinnen om te onderzoeken waar de missende index(waarde) is

for i in range(1, len(XY_sorted)):
    returnXY = np.log(XY_sorted[i][1] / XY_sorted[i-1][1])
    print(returnXY)
    XY_return.append(returnXY)

minimum = np.amin(XY_return)
maximum = np.amax(XY_return)
print("\n", "\n")
print("minimum is ", minimum, "maximum is ", maximum)

"""
#If we want to normalize the returns

minimum_ret = np.amin(Z_return)
maximum_ret = np.amax(Z_return)

for i in range(1, len(Z_return)):
    c = 10*((Z_return[i] - minimum_ret) / (maximum_ret - minimum_ret))
    normalized_Z.append(c)

normalized_Z_return = np.asarray(normalized_Z, dtype=np.int64)
"""

