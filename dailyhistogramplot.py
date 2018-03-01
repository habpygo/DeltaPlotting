from datetime import datetime
from datetime import timedelta
import sys
import math
import matplotlib as mplt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from numpy import NaN, Inf, arange, isscalar, asarray, array
import matplotlib.cm as cm
from pandas.tools.plotting import bootstrap_plot

"""
  % This program finds the Hi's and Low's for any tradeble commondity, security or currency
  % The data file must be a tab seperated txt file. Usually this file is preparated from a
  % CSV file with Excel. The data format is:
  %    0     1    2    3  4  5   6
  %   Year Month Day Open Hi Lo Close
  % After the file has been read, the values will be split, divided by Fourier color and
  % captured in separate arrays (e.g. Red_X of Orange_Z). The values (_Z array) are then
  % fed into the peakdet() function to determine the hi and low and their date and time

  % You can choose between two filtering techniques:
  % Cut-off will measure a hi or lo when a certain value is trespassed.
  % Filter will consider some value a hi or lo when the change between the previous
  % turning point and the hi/lo will supercede a the given value


  This program was written by Harry Boer (harryaboer@gmail.com)
"""

datafile = "EuroDollarDaily.txt"

#delta = float(input("What is the delta?\n"))
delta = 0.01
#my_filter = input('Which filtering technique is required, Cut-off(c) or Filter(f)\n')
my_filter = 'f'
#kleurvdd = input("Wat is de kleur van de dag? g, r, b or o\n")
kleurvdd = 'o'
max_or_min = input("Do you want to investigate only max(max), only min(min), both(enter), or stacked(s)\n")
#max_or_min = "s"

#bins = int(input("How many bins?\n"))
bins = 24

Y = []
periods_per_day = bins
Red_X=[]; Red_Y=[]; Red_Z=[]; Red_tijd=[]; Blue_X=[]; Blue_Y=[]; Blue_Z=[]; Blue_tijd=[]
Orange_X=[]; Orange_Y=[]; Orange_Z=[]; Orange_tijd=[]; Green_X=[]; Green_Y=[]; Green_Z=[]; Green_tijd=[]
Choosen_array_X = [] ; Choosen_array_Y = [] ; Choosen_array_Z = [] ; Choosen_array_tijd=[]
datum_array = [] ; close_array = [] ; datum_num_array = []

def peakdet(v, delta, cut_off, x = None):
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

    if cut_off == 'c':
        delta_cutoff = delta
        delta_filter = 0
    elif cut_off == 'f':
        delta_cutoff = 0
        delta_filter = delta

    lookformax = True

    for i in arange(len(v)):
        this = v[i]
        if this > mx-delta_cutoff:
            mx = this
            mxpos = x[i]
        if this < mn+delta_cutoff:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx-delta_filter:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta_filter:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)
# WE MOETEN NIET == MAAR < OF > GEBRUIKEN

start_Red_day = datetime(2003, 3, 18)
start_Blue_day = datetime(2003, 6, 14)
start_Orange_day = datetime(2003, 9, 10)
start_Green_day = datetime(2003, 12, 8)

def kleur_bepaler(datum):
    result = (datum - start_Red_day).total_seconds()
    #if result % 7081862 == 0:
    if datum > start_Red_day and datum < start_Blue_day:
        # 345600 seconds equals 4 days, one siderial moon orbit equals 2,360,620.8 seconds
        # 3 siderial moon orbits equals 7081862.4 seconds
        print("Voor datum" , datum, "The result was Red")
        return "Red"
    if datum > start_Blue_day and datum < start_Orange_day:
        print("Voor datum ", datum, "The result was Blue")
        return "Blue"
    if datum > start_Orange_day and datum < start_Green_day:
        print("Voor datum ", datum, "The result was Orange")
        return "Orange"
    if datum > start_Green_day and datum < start_Red_day:
        print("Voor datum ", datum, "The result was Green")
        return "Green"
    #else:
    #    print('Geen kleur gevonden')

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
    datum_array.append(datum)
    x_num = mplt.dates.date2num(datum)
    datum_num_array.append(x_num)
    Close = float(line.split()[6].strip('\n'))
    close_array.append(Close)

#at this point we have read data from file and created three arrays filled with dates, closes and numeric dates

    if kleur_bepaler(datum) == "Red": # replace datum with x_num etc.
        #print("Red kleur gevonden")
        Red_X.append(x_num) #file doesn't contain hour-minutes-seconds data
        Red_Z.append(Close)
    elif kleur_bepaler(datum) == "Blue":
        #print("Blue kleur gevonden")
        Blue_X.append(x_num)
        Blue_Z.append(Close)
    elif kleur_bepaler(datum) == "Orange":
        #print("Orange kleur gevonden")
        Orange_X.append(x_num)
        Orange_Z.append(Close)
    else:
        #print("Green kleur gevonden")
        Green_X.append(x_num)
        Green_Z.append(Close)

currency_file.close()

plt.close('all')

def dag_kleur(daycolor):
    global print_kleur
    if daycolor == "g":
        Choosen_array_X = Green_X
        Choosen_array_Z = Green_Z
        #print('lengte Choosen_array_Z is ', len(Choosen_array_Z), 'lengte Green_Z is', len(Green_Z))
        print_kleur = "Green"
    elif daycolor == "r":
        Choosen_array_X = Red_X
        Choosen_array_Z = Red_Z
        print_kleur = "Red"
    elif daycolor == "b":
        Choosen_array_X = Blue_X
        Choosen_array_Z = Blue_Z
        print_kleur = "Blue"
    elif daycolor == "o":
        Choosen_array_X = Orange_X
        Choosen_array_Z = Orange_Z
        print_kleur = "Orange"

    return Choosen_array_X,Choosen_array_Z

XX,ZZ = dag_kleur(kleurvdd) #stopt the Green,Red,Blue,Orange arays in the Choosen arrays

######--FIND THE HI's AND LOW's--###########
[maxarray,minarray]=peakdet(ZZ, delta, my_filter, XX)     # selecteerd hi's en low's op value en geeft twee
############################################   # arrays terug met tijd en value

print('length maxarray is ', len(maxarray), 'and length minarray is ', len(minarray))
#print(maxarray)

max_X = []; max_Z = []; min_X = []; min_Z = []; Z_return = []
normalized_Z = [] ; normalized_Z_return = [] ; Z_return_percentage = []

def dag_tijd_splitter(dag_tijd_in_nummers): #split de dag waarde van de uren-minuten0-seconden
    tijd, dag = math.modf(dag_tijd_in_nummers)
    tijd = tijd * 24 #in hours and decimal minutes
    return(dag)

Z_max_min = np.concatenate((maxarray,minarray), axis=0)
Z_max_min_sorted = Z_max_min[np.argsort(Z_max_min[:, 0])] #all the rows, only the first column

mxnumerictime = maxarray[:, 0]
mnnumerictime = minarray[:, 0]
numerictime = Z_max_min_sorted[:, 0]

max_dag_array = [] #wordt niet gebruikt
min_dag_array = [] #wordt niet gebruikt
combined_dag_array = []

for waarde in mxnumerictime:
    mxtijdwaarde=dag_tijd_splitter(waarde)
    max_dag_array.append(mxtijdwaarde)

for waarde in mnnumerictime:
    mntijdwaarde=dag_tijd_splitter(waarde)
    min_dag_array.append(mntijdwaarde)

for waarde in numerictime:
    dagwaarde=dag_tijd_splitter(waarde)
    combined_day_array.append(dagwaarde)

#feed the pandas
pd_maxDag = pd.DataFrame(max_dag_array)
pd_minDag = pd.DataFrame(min_dag_array)
plot_dag = mplt.dates.num2date(numerictime)
pd_plot_dag = pd.DataFrame(plot_dag)
Combined_Dag = pd.DataFrame(combined_day_array)
Value = pd.DataFrame(Z_max_min_sorted[:, 1])


maxmin_Dag_Value = pd.concat([pd_maxDag,pd_minDag], axis=1)
maxmin_Dag_Value.columns = ['maxima','minima']

Dag_Value = pd.concat([pd_plot_dag, Value], axis=1)
Dag_Value.colums = ['Dag','Value']
print(Tijd_Value)
#combinedXYZ.to_csv("myfile.csv") #print naar csv file

#PLOTTING THE HISTOGRAMS
if max_or_min == "s": #plot stacked histogram
    combined_df = pd.DataFrame({'Maxima': max_tijd_array, 'Minima': min_tijd_array},columns=['Maxima', 'Minima'])
    combined_df.plot(kind='hist', stacked=True, bins = bins)
    plt.title("%s - Maxima and Minima:  %s delta and %s bins" %(print_kleur,delta,bins))
    plt.show()
elif max_or_min == "max": #plot de maxima
    pd_maxTijd.plot(kind='hist', bins=bins, facecolor=print_kleur)
    plt.title("%s - Maxima filtered with %s delta and with %s bins" %(print_kleur,delta,bins))
    plt.show()
elif max_or_min == "min": #plot de minima
    pd_minTijd.plot(kind='hist', bins=bins, facecolor=print_kleur)
    plt.title("%s - Minima filtered with %s delta and with %s bins" %(print_kleur,delta,bins))
    plt.show()
else: #plot beide grafieken tegelijkertijd
    pd_maxTijd.plot(kind='hist', bins=bins, facecolor=print_kleur)
    plt.title("%s - Maxima filtered with %s delta and with %s bins" %(print_kleur,delta,bins))
    pd_minTijd.plot(kind='hist', bins=bins, facecolor=print_kleur)
    plt.title("%s - Minima filtered with %s delta and with %s bins" %(print_kleur,delta,bins))
    plt.show()

print('Eerste datum is', first_datum, 'de kleur is', kleurvdd, 'de file is', currency_file)
