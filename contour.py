from datetime import datetime
from datetime import timedelta
import sys
import matplotlib
import matplotlib as mplt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy import NaN, Inf, arange, isscalar, asarray, array
import matplotlib.cm as cm
from pandas.tools.plotting import bootstrap_plot

#delta = float(input("What is the delta?\n"))
delta = 0.0015

#max_or_min = input("Do you want to investigate only max, only min, both, or stacked. Press max, min, s, or enter\n")

#bins = int(input("How many bins?\n"))
#bins = 24

Y = []
periods_per_day = 96
Red_X = [] ; Red_Y = [] ; Red_Z = [] ; Blue_X = [] ; Blue_Y = [] ; Blue_Z = []
Orange_X = [] ; Orange_Y = [] ;Orange_Z = [] ; Green_X = [] ; Green_Y = [] ; Green_Z = []


start_Red_day = datetime(2012, 3, 1) # 1 maart 2012 was een Rood jaar
start_Blue_day = datetime(2012, 3, 2)
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
    %        delta, or value * (1 + delta), or value * (1 - delta).

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

    if delta < 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN

    lookformax = True

    for i in arange(len(v)):
        this = v[i]
        if this > mx * (1 - (0.75 * delta)):
            mx = this
            mxpos = x[i]
        if this < mn * (1 + delta):
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)

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
datafile = "29sep2015.txt"
#datafile = "euro-15minute.txt"

# Vind de eerste datum uit de file
currency_file = open(datafile)
count = 0
for line in currency_file:
    if count == 1:
        break
    else:
        first_datum = datetime(int(line.split('\t')[0]), int(line.split('\t')[1]), int(line.split('\t')[2]))
        count += 1

currency_file.close()

currency_file = open(datafile)

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

currency_file.close()

print("Eerste datum is ", first_datum)
plt.close('all')

#FIND THE HI's AND LOW's
[maxarray,minarray]=peakdet(Green_Z, delta)

max_X = [] ; max_Y = [] ; max_Z = [] ; min_X = [] ; min_Y = [] ; min_Z = [] ; Z_return = []
normalized_Z = [] ; normalized_Z_return = [] ; Z_return_percentage = []

for max_lists in maxarray:
    index = int(max_lists[0])
    max_X.append(Green_X[index])
    max_Y.append(Green_Y[index])
    max_Z.append(Green_Z[index])

for min_lists in minarray:
    index = int(min_lists[0])
    min_X.append(Green_X[index])
    min_Y.append(Green_Y[index])
    min_Z.append(Green_Z[index])

X_combined = np.concatenate((max_X, min_X), axis=0)
Y_combined = np.concatenate((max_Y, min_Y), axis=0)
Z_max_min = np.concatenate((maxarray,minarray), axis=0)

Z_return.append(0.0)
Z_max_min_sorted = Z_max_min[np.argsort(Z_max_min[:, 0])] #all the rows, only the first column
for i in range(1, len(Z_max_min_sorted)):
    Z_return.append(np.log(Z_max_min_sorted[i][1] / Z_max_min_sorted[i-1][1]))

for i in range(1, len(Z_max_min_sorted)):
    Z_return_percentage.append((Z_max_min_sorted[i][1] - Z_max_min_sorted[i-1][1])
                                   /Z_max_min_sorted[i-1][1])

# Make Pandas DataFrames
X_pd_max = pd.DataFrame(max_X)
X_pd_min = pd.DataFrame(min_X)
Y_pd_max = pd.DataFrame(max_Y)
Y_pd_min = pd.DataFrame(min_Y)

X_pandas = pd.DataFrame(X_combined)
Y_pandas = pd.DataFrame(Y_combined)
Z_pd_value = pd.DataFrame(Z_max_min_sorted[:, 1])
Z_pd_return = pd.DataFrame(Z_return) # was normalized_Z_return
Z_pandas_perc = pd.DataFrame(Z_return_percentage)

#Combine the different arrays
combinedY = pd.concat([Y_pd_max, Y_pd_min], axis=1)
combinedXYZ = pd.concat([X_pandas, Y_pandas, Z_pd_value, Z_pd_return, Z_pandas_perc], axis=1)
combinedXYZ.columns = ['X-value', 'Y-value', 'Z-value', 'Z-return', 'Z-return-%']
combined_df = pd.DataFrame({'Maxima': max_Y, 'Minima': min_Y} , columns=['Maxima', 'Minima'])

#PLOTTING THE RESULTS
#combinedXYZ.plot(kind='scatter', colormap='seismic', x='X-value', y='Y-value', c='Z-return-%', s=20)

#Z_pd_return.plot(kind='box') #whisker plot
#Z_pd_return.plot(kind='kde') #density plot
#combinedXYZ.plot(kind='hexbin', x='X value', y='Y value', gridsize=25) #hexbin plot
#Z_pd_return.plot(kind='hist', stacked=True, bins=96) #histogram of returns
#Y_pandas.plot(kind='hist', stacked=True, bins=96)

#plt.show()
Z_sliced = Z_max_min_sorted[:, 1]
print("X_combined shape ", X_combined.shape, type(X_combined), "Y_combined ", Y_combined.shape,
      type(Y_combined), "Z_max_min_sorted shape is", Z_sliced.shape, type(Z_sliced))

plt.figure()
CS = plt.contour(X_combined, Y_combined, Z_sliced)
plt.clabel(CS, inline=1, fontsize=10)
plt.title('Contour plot')
plt.show()
'''
if max_or_min == "s": #plot stacked
    combined_df.plot(kind='hist', stacked=True, bins = bins)
    plt.title("Maxima and Minima stacked with %s delta and %s bins" %(delta,bins))
    plt.show()
elif max_or_min == "max": #plot de maxima
    Y_pd_max.plot(kind='hist', bins=bins)
    plt.title("Maxima filtered with %s delta and with %s bins" %(delta,bins))
    plt.legend
    plt.show()
elif max_or_min == "min": #plot de minima
    Y_pd_min.plot(kind='hist', bins=bins)
    plt.title("Minima filtered with %s delta and with %s bins" %(delta,bins))
    plt.show()
else: #plot beide grafieken tegelijkertijd
    Y_pd_max.plot(kind='hist', bins=bins)
    plt.title("Maxima filtered with %s delta and with %s bins" %(delta,bins))
    Y_pd_min.plot(kind='hist', bins=bins)
    plt.title("Minima filtered with %s delta and with %s bins" %(delta,bins))
    plt.show()
'''
