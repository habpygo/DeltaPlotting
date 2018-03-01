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
  %    0     1    2    3      4     5   6  7   8
  %   Year Month Day Hours Minutes Open Hi Lo Close
  % After the file has been read, the values will be split, divided by Fourier color and
  % captured in separate arrays (e.g. Red_X of Orange_Z). The values (_Z array) are then
  % fed into the peakdet() function to determine the hi and low and their date and time
  % You can choose between two filtering techniques:
  % Cut-off will measure a hi or lo when a certain value is trespassed.
  % Filter will consider some value a hi or lo when the change between the previous
  % turning point and the hi/lo will supercede a the given value


  This program was written by Harry Boer (harryaboer@gmail.com)
"""
#beste waarden zijn: delta=0.0008, my_filter=f, bins=24

#datafile = "29sep2015.txt"
datafile = "euro-15minute.txt"

delta = float(input("What is the delta?\n"))
#delta = 0.0008
my_filter = input('Which filtering technique is required, Cut-off(c) or Filter(f)\n')
kleurvdd = input("Wat is de kleur van de dag? g, r, b or o\n")
#kleurvdd = 'o'
#bins = int(input("How many bins?\n"))
bins = 24

Red_X=[]; Red_Y=[]; Red_Z=[]; Red_tijd=[]; Blue_X=[]; Blue_Y=[]; Blue_Z=[]; Blue_tijd=[]
Orange_X=[]; Orange_Y=[]; Orange_Z=[]; Orange_tijd=[]; Green_X=[]; Green_Y=[]; Green_Z=[]; Green_tijd=[]
Choosen_array_X = [] ; Choosen_array_Y = [] ; Choosen_array_Z = [] ; Choosen_array_tijd=[]


start_Red_day = datetime(2012, 3, 1) # 1 maart 2012 was een Rood jaar
start_Blue_day = datetime(2012, 3, 2)
start_Orange_day = datetime(2012, 3, 3) # 2012 was een schrikkeljaar; 2016 ook
start_Green_day = datetime(2012, 3, 4)

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
    if kleur_bepaler(datum) == "Red": # replace datum with x_num etc.
        #print("Red kleur gevonden")
        Red_X.append(x_num)
        Red_Y.append(y_num - x_num) #tijdsverschil
        Red_Z.append(Close)
        Red_tijd.append(y_num) #werkelijke tijd
    elif kleur_bepaler(datum) == "Blue":
        #print("Blue kleur gevonden")
        Blue_X.append(x_num)
        Blue_Y.append(y_num - x_num)
        Blue_Z.append(Close)
        Blue_tijd.append(y_num)
    elif kleur_bepaler(datum) == "Orange":
        #print("Orange kleur gevonden")
        Orange_X.append(x_num)
        Orange_Y.append(y_num - x_num)
        Orange_Z.append(Close)
        Orange_tijd.append(y_num)
    else:
        #print("Green kleur gevonden")
        Green_X.append(x_num)
        Green_Y.append(y_num - x_num)
        Green_Z.append(Close)
        Green_tijd.append(y_num)

currency_file.close()

plt.close('all')

def dag_kleur(daycolor):
    global print_kleur
    if daycolor == "g":
        Choosen_array_X = Green_X
        Choosen_array_Y = Green_Y
        Choosen_array_Z = Green_Z
        Choosen_array_tijd = Green_tijd
        #print('lengte Choosen_array_Z is ', len(Choosen_array_Z), 'lengte Green_Z is', len(Green_Z))
        print_kleur = "Green"
    elif daycolor == "r":
        Choosen_array_X = Red_X
        Choosen_array_Y = Red_Y
        Choosen_array_Z = Red_Z
        Choosen_array_tijd = Red_tijd
        print_kleur = "Red"
    elif daycolor == "b":
        Choosen_array_X = Blue_X
        Choosen_array_Y = Blue_Y
        Choosen_array_Z = Blue_Z
        Choosen_array_tijd = Blue_tijd
        print_kleur = "Blue"
    elif daycolor == "o":
        Choosen_array_X = Orange_X
        Choosen_array_Y = Orange_Y
        Choosen_array_Z = Orange_Z
        Choosen_array_tijd = Orange_tijd
        print_kleur = "Orange"

    return Choosen_array_X,Choosen_array_Y,Choosen_array_Z,Choosen_array_tijd

XX,YY,ZZ,TT = dag_kleur(kleurvdd) #stopt the Green,Red,Blue,Orange arays in the Choosen arrays

######--FIND THE HI's AND LOW's--###########
[maxarray,minarray]=peakdet(ZZ, delta, my_filter, TT)     # selecteerd hi's en low's op value en geeft twee
############################################   # arrays terug met tijd en value

max_X = []; max_Y = []; max_Z = []; max_T = []; min_X = []; min_Y = []; min_Z = []; min_T = []; Z_return = []
normalized_Z = [] ; normalized_Z_return = [] ; Z_return_percentage = []

def dag_tijd_splitter(dag_tijd_in_nummers): #split de dag waarde van de uren-minuten0-seconden
    tijd, dag = math.modf(dag_tijd_in_nummers)
    tijd = tijd * 24 #in hours and decimal minutes
    return(tijd,dag)

Z_max_min = np.concatenate((maxarray,minarray), axis=0)
Z_max_min_sorted = Z_max_min[np.argsort(Z_max_min[:, 0])] #all the rows, only the first column

mxnumerictime = maxarray[:, 0]
mnnumerictime = minarray[:, 0]
numerictime = Z_max_min_sorted[:, 0]

max_tijd_array = []
max_dag_array = []
min_tijd_array = []
min_dag_array = []
combined_tijd_array = []
combined_dag_array = []

for waarde in mxnumerictime: #fill the maximum tijd array
    mxtijdwaarde,mxdagwaarde=dag_tijd_splitter(waarde)
    max_tijd_array.append(mxtijdwaarde)
    max_dag_array.append(mxdagwaarde)

for waarde in mnnumerictime: #fill the minimum tijd array
    mntijdwaarde,mndagwaarde=dag_tijd_splitter(waarde) # min_tijd_array.append(dag_tijd_splitter(waarde))
    min_tijd_array.append(mntijdwaarde)
    min_dag_array.append(mndagwaarde)

for waarde in numerictime: #fill the combined tijd array
    tijdwaarde,dagwaarde=dag_tijd_splitter(waarde)
    combined_tijd_array.append(tijdwaarde)
    combined_dag_array.append(dagwaarde)

#feed the pandas
pd_maxTijd = pd.DataFrame(max_tijd_array)
pd_minTijd = pd.DataFrame(min_tijd_array)
pd_maxDag = pd.DataFrame(max_dag_array)
pd_minDag = pd.DataFrame(min_dag_array)

pd_minArray = pd.concat([pd_minDag,pd_minTijd], axis=1)
pd_minArray.columns = ['Dag','Tijd']
pd_maxArray = pd.concat([pd_maxDag,pd_maxTijd], axis=1)
pd_maxArray.columns = ['Dag','Tijd']

plot_tijd = mplt.dates.num2date(numerictime)
pd_plot_tijd = pd.DataFrame(plot_tijd)

Combined_Dag = pd.DataFrame(combined_dag_array)
Combined_Tijd = pd.DataFrame(combined_tijd_array)
Value = pd.DataFrame(Z_max_min_sorted[:, 1])

maxmin_Tijd_Value = pd.concat([pd_maxTijd,pd_minTijd], axis=1)
maxmin_Tijd_Value.columns = ['maxima','minima']


ax = pd_minArray.plot(kind='scatter', x='Dag', y='Tijd', color='Red', label='Low values',
                      figsize=(17,10)) # marker = '.'
pd_maxArray.plot(kind='scatter', x='Dag', y='Tijd', color='Green', label='Hi values', ax=ax, grid=True)
plt.title("%s - Minima and maxima filtered with %s delta and with %s bins" %(print_kleur,delta,bins))
plt.gca().invert_yaxis() # invert the y-ax in order to compare with the Excel spread sheet 
plt.show()


