from datetime import datetime
from datetime import timedelta
import time
import matplotlib as mplt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy import NaN, Inf, arange, isscalar, asarray, array
from scipy import signal
from scipy.signal import argrelextrema, argrelmax, argrelmin

Y = []
periods_per_day = 96
Red_X = [] ; Red_Y = [] ; Red_Z = [] ; Blue_X = [] ; Blue_Y = [] ; Blue_Z = []
Orange_X = [] ; Orange_Y = [] ;Orange_Z = [] ; Green_X = [] ; Green_Y = [] ; Green_Z = []
Red_tijdsverschil = []; Blue_tijdsverschil = []; Orange_tijdsverschil = []; Green_tijdsverschil = []

start_Red_day = datetime(2012, 3, 1)
start_Blue_day = datetime(2012, 3, 2) # 1 maart 2012 was een Rood jaar
start_Orange_day = datetime(2012, 3, 3) # 2012 was een schrikkeljaar; 2016 ook
start_Green_day = datetime(2012, 3, 4)

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

    % Eli Billauer, 3.4.05 (Explicitly not copyrighted).
    % This function is released to the public domain; Any use is allowed.

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

    mn, mx = Inf, -Inf # mx word minus infinity en groeit vanaf daar
    mnpos, mxpos = NaN, NaN

    lookformax = True

    for i in arange(len(v)): # Python for " for i=1, i<=arraylengte, i++
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax: # hier wordt gefilterd 'if lookformax == True'
            if this < mx*(1-(0.75*delta)): # was 'if this < mx-delta', nu in %
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn*(1+delta):
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)

# We hebben nu de maxtab array met maxima en de mintab array met minima
# We zouden ze nu samen kunnen voegen en alleen de relevante (belangrijkste)
# Hi's and Low's er uit moeten pikken, i.e. de ruis onderdrukken

def ruis_onderdrukker(maxima, minima, filter):
    filtered_maxima = [] ; filtered_minima = []
    # code here


    return array(filtered_maxima), array(filtered_minima)

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

counter = 1

# Vind de eerste datum uit de file
currency_file = open('euro-15minute.txt')
count = 0
for line in currency_file:
    if count == 1:
        break
    else:
        first_datum = datetime(int(line.split('\t')[0]), int(line.split('\t')[1]), int(line.split('\t')[2]))
        count += 1

currency_file.close()

currency_file = open('euro-15minute.txt')

# VOLGENS MIJ MOET ER EEN IF STATEMENT KOMEN NA REGEL 133 GELIJKWAARDIG AAN DE MODULUS '%' STATEMENT
# IN DE kleur_bepaler FUNCTIE
for line in currency_file: # values separated by tabs ('\t') test.txt
    datum = datetime(int(line.split('\t')[0]), int(line.split('\t')[1]), int(line.split('\t')[2]))
    x_num = mplt.dates.date2num(datum)
    tijd = datetime(int(line.split('\t')[0]), int(line.split('\t')[1]),
                    int(line.split('\t')[2]), int(line.split('\t')[3]), int(line.split('\t')[4]))
    y_num = mplt.dates.date2num(tijd)
    Close = float(line.split()[8].strip('\n'))
    Y.append(Close)
    tijdsverschil = (tijd - datum).total_seconds() #900 bij optellen om aan 24hr(=86400secs) te komen
    if kleur_bepaler(datum) == "Red": # replace datum with x_num etc.
        #print("Red kleur gevonden")
        Red_X.append(x_num)
        Red_Y.append(y_num - x_num)
        Red_Z.append(Close)
        Red_tijdsverschil.append(tijdsverschil)
    elif kleur_bepaler(datum) == "Blue":
        #print("Blue kleur gevonden")
        Blue_X.append(x_num)
        Blue_Y.append(y_num - x_num)
        Blue_Z.append(Close)
        Blue_tijdsverschil.append(tijdsverschil)
    elif kleur_bepaler(datum) == "Orange":
        #print("Orange kleur gevonden")
        Orange_X.append(x_num)
        Orange_Y.append(y_num - x_num)
        Orange_Z.append(Close)
        Orange_tijdsverschil.append(tijdsverschil)
    else:
        #print("Green kleur gevonden")
        Green_X.append(x_num)
        Green_Y.append(y_num - x_num)
        Green_Z.append(Close)
        Green_tijdsverschil.append(tijdsverschil)

currency_file.close()

print("Eerste datum is ", first_datum)
plt.close('all')

[maxarray,minarray]=peakdet(Green_Z, 0.0025) #best Delta is 0.0015

max_X = []
max_Y = []
min_X = []
min_Y = []
Green_Y_array = []

for max_lists in maxarray:
    index = int(max_lists[0])
    max_X.append(Green_X[index])
    max_Y.append(Green_tijdsverschil[index])

for min_lists in minarray:
    index = int(min_lists[0])
    min_X.append(Green_X[index])
    min_Y.append(Green_tijdsverschil[index])

plot_Y = []
for item in max_Y:
    plot_Y.append(item/900)
    print(item/900)


# the histogram of the data
n, bins, patches = plt.hist(plot_Y, 96, facecolor='green', alpha=0.75)

plt.xlabel('15-minute intervals')
plt.ylabel('Frequency')
plt.title('Green maxima')
plt.grid(True)

plt.show()

