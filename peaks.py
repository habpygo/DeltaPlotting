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
  % This program performs a Monte Carlo simulatio on a predifined data set
  % The data file must be a tab seperated txt file. Usually this file is preparated from a
  % CSV file with Excel. The data format is:
  %    0     1    2    3      4     5   6  7   8
  %   Year Month Day Hours Minutes Open Hi Lo Close
  % After the file has been read, the values will be split.

  This program was written by Harry Boer (harryaboer@gmail.com)
"""
datafile = "Edelweis.txt"
simulatie_file = open(datafile,'r')

for line in simulatie_file: # values separated by tabs ('\t') test.txt
    simulatie_file.close()

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

XX,YY,ZZ,TT = dag_kleur(kleurvdd) #stopt the Green,Red,Blue,Orange arays in the four Choosen arrays

######--FIND THE HI's AND LOW's--###########
[maxarray,minarray]=peakdet(ZZ, delta, my_filter, TT)     # selecteerd hi's en low's op value en geeft twee
############################################   # arrays terug met tijd en value

print('length maxarray is ', len(maxarray), 'and length minarray is ', len(minarray))
#print(maxarray)

max_X = []; max_Y = []; max_Z = []; max_T = []; min_X = []; min_Y = []; min_Z = []; min_T = []; Z_return = []
normalized_Z = [] ; normalized_Z_return = [] ; Z_return_percentage = []

def dag_tijd_splitter(dag_tijd_in_nummers): #split de dag waarde van de uren-minuten0-seconden
    tijd, dag = math.modf(dag_tijd_in_nummers)
    tijd = tijd * 24 #in hours and decimal minutes
    return(tijd)

Z_max_min = np.concatenate((maxarray,minarray), axis=0)
Z_max_min_sorted = Z_max_min[np.argsort(Z_max_min[:, 0])] #all the rows, only the first column

mxnumerictime = maxarray[:, 0]
mnnumerictime = minarray[:, 0]
numerictime = Z_max_min_sorted[:, 0]

max_tijd_array = []
#max_dag_array = [] #wordt niet gebruikt
min_tijd_array = []
#min_dag_array = [] #wordt niet gebruikt
combined_tijd_array = []
combined_dag_array = []

for waarde in mxnumerictime:
    mxtijdwaarde=dag_tijd_splitter(waarde)
    #if mxtijdwaarde == NaN:
    #    mxtijdwaarde = 23.15
    max_tijd_array.append(mxtijdwaarde)

for waarde in mnnumerictime:
    mntijdwaarde=dag_tijd_splitter(waarde)
    #if mntijdwaarde == NaN:
    #    mntijdwaarde = 23.15
    min_tijd_array.append(mntijdwaarde)

for waarde in numerictime:
    tijdwaarde=dag_tijd_splitter(waarde)
    combined_tijd_array.append(tijdwaarde)

'''
if len(max_tijd_array) > len(min_tijd_array):
    min_tijd_array.append(23.55)
elif len(min_tijd_array) > len(max_tijd_array):
    max_tijd_array.append(23.55)
'''
#feed the pandas
pd_maxTijd = pd.DataFrame(max_tijd_array)
pd_minTijd = pd.DataFrame(min_tijd_array)
plot_tijd = mplt.dates.num2date(numerictime)
pd_plot_tijd = pd.DataFrame(plot_tijd)
Combined_Tijd = pd.DataFrame(combined_tijd_array)
Value = pd.DataFrame(Z_max_min_sorted[:, 1])


maxmin_Tijd_Value = pd.concat([pd_maxTijd,pd_minTijd], axis=1)
maxmin_Tijd_Value.columns = ['maxima','minima']
print(maxmin_Tijd_Value)
print('----------------')
print('length max_tijd_array is', len(max_tijd_array), 'length min_tijd_array is',len(min_tijd_array))
print('length pd_maxTijd is', len(pd_maxTijd), 'length pd_minTijd is',len(pd_minTijd))

Tijd_Value = pd.concat([pd_plot_tijd, Value], axis=1)
Tijd_Value.colums = ['Tijd','Value']
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
