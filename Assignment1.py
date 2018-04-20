# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 16:55:17 2018

@author: Hesiris
"""

import csv;
import numpy as np;
#%% Load data
patients = {}
#using a dictionary approach means that if the input data order or attributes 
#changed, the algorithm is still able to cope with it
#It also makes a faster data insertion if the any of the fields are not ordered.
#E.g. Having the patient ID not in order would result in O(n) for each insertion
#in a matrix. Using a hash table results in lim->O(1)
with open('dataset_mood_smartphone.csv') as csvfile:
    r = csv.reader(csvfile,quotechar='"')
    k=1
    next(r)
    for row in r:
        #The dictionary should have the format of
        #patients[id][date][time][attrib]=val
        id = row[1]
        date = row[2][:10]
        time = row[2][11:]
        attr = row[3]
        try:
            val = float(row[4])
            #if val==0 and attr!='activity':
             #   print('%s%s,%s,%s,%f'%(id,date,time,attr,val))
        except:
            #if invalid value is detected e.g. NA, it skips that value
            continue;
        #The algorithm tries to access the dictionary field.
        #If it fails, it attempts to create the last field.
        #if that fails, it attempts to create the previous one, and so on
        try:
            patients[id] [date] [attr] [time] = val 
        except:
            try:
                patients[id] [date] [attr] = {}
                patients[id] [date] [attr] [time]  = val
            except:
                try:
                    patients[id] [date] = {}
                    patients[id] [date] [attr] = {}
                    patients[id] [date] [attr] [time]= val
                except:
                    patients[id] = {}
                    patients[id] [date]={}
                    patients[id] [date] [attr] ={ }
                    patients[id] [date] [attr] [time] = val
                    
        k+=1
        #if k>6000:
        #    break;
            
#%% Create average for days and reallocate as such
from datetime import datetime
#var for next section
ndays = 0;
nregr=5;

for patient in patients:
    ndaysprev = ndays
    sortedDays=sorted(patients[patient].keys())
    firstDay= datetime.strptime(sortedDays[0], '%Y-%m-%d')
    lastDay = datetime.strptime(sortedDays[-1], '%Y-%m-%d')
    ndays = (lastDay - firstDay).days
    
    for day in patients[patient]:
        ndaysprev=ndays;
        timeSlots = np.zeros(24)
        
        attribs = list(filter(lambda x: '_count' not in x, patients[patient][day].keys()))
        for attrib in attribs:
            S=0.0
            countTimes=0.0
            for time in patients[patient][day][attrib]:
                S+=patients[patient][day][attrib][time]
                countTimes+=1;
                if attrib in ['appCat.social','appCat.game','appCat.entertainment' \
                              ,'appCat.weather','appCat.communication','call','sms']:
                    timeSlots[int(time[:2])]=1;
            patients[patient][day][attrib] = S
            patients[patient][day][attrib+'_count'] = countTimes
            patients[patient][day]['sleep'] = sum(timeSlots)
            patients[patient][day]['nightlife'] = any(timeSlots[:7])
    #ndays-=nregr;
    ndays=max(ndays,ndaysprev)
            
#%% Convert into a table optimized for statistical analysis
# All the computational advantages mentioned in section 1 are now removed by
# converting it into a table, but is (to be seen) easier to code for statistical
# analysis
            

#NOTE: next(iter(patients.values())) can be used ot access first element
target = 'mood'
attributeList = ['mood',
 'screen',
 'appCat.builtin',
 'appCat.communication',
 'appCat.entertainment',
 'activity',
 'appCat.social',
 'appCat.other',
 'circumplex.arousal',
 'circumplex.valence',
 'appCat.office',
 'call',
 'appCat.travel',
 'appCat.utilities',
 'sms',
 'appCat.finance',
 'appCat.unknown',
 'appCat.game',
 'appCat.weather',
 'sleep',
 'nightlife']

#Sleep and nighlife not included, that do not have a count
for i in range(len(attributeList)-2):
    attributeList.insert(i*2+1,attributeList[i*2]+'_count')
nattribs = len(attributeList)


ndays+=1;
npatients = len(patients.keys())
patientTable = np.zeros([npatients,ndays,nattribs])
patientTable[:] = np.nan
indD=0;
for indPatient,patient in enumerate(patients):
    indDay = -1
    
    sortedDays=sorted(patients[patient].keys())
    for day in sortedDays:    
        if indDay==-1:
            prevDay = day
            indDay=0;
        else:
            currDate = datetime.strptime(day, '%Y-%m-%d')
            prevDate = datetime.strptime(prevDay, '%Y-%m-%d')
            indDay += (currDate - prevDate).days
            prevDay = day;

        for attr in patients[patient][day]:
            indAttr = attributeList.index(attr)        
            patientTable[indPatient][indDay][indAttr] = patients[patient][day][attr]
#%% plot two of the attributes to see visually check results
import matplotlib.pyplot as plt
def plotPatients(patientTable,attributeList):
    npatients= patientTable.shape[0]
    nattribs=patientTable.shape[2]
    for i in range(npatients):
        print('Patient %d'%i)
        plt.figure(figsize=(14,25))
        for j in range(nattribs):
            plt.subplot(np.ceil(nattribs/3),3,j+1)
            plt.plot(range(len(patientTable[i,:,j])),patientTable[i,:,j])
            plt.title(attributeList[j])
            plt.ylabel('Mean Value')
            plt.xlabel('Time')
    
        plt.tight_layout()
        plt.show()
    return

#%%
plotPatients(patientTable[:1][:][:],attributeList);
#%%

def reduceTableSize(table,maxNanCount=.35,entryLimit = 3):
    height = table.shape[0]
    width = table.shape[1]
    
    start = 0
    end = height;
    isStartFound = False;
    prev = []
    
    def isAcceptable(i):
        return np.count_nonzero(np.isnan(table[i-entryLimit:i]))<(width*entryLimit)*maxNanCount
    
    for i in range(entryLimit):
        prev.append(isAcceptable(i))
    
    #deque may provide slightly better performance, but the amount of days does not\
    #warrant the additional readablility hindrance
    for i in range(entryLimit,height):
        prev.pop(0)
        prev.append(isAcceptable(i))
        #check if more than 30% of the data is missing fromt he last entryLimit rows
        #if not that much data missing, the true array starts from there
        if not isStartFound and prev.count(True)==entryLimit:
            start = i-3
            isStartFound = True
        #If the last three rows had more than 30% empty, that's the end
        if isStartFound and prev.count(False)==entryLimit:
            end = i
            break;
            
    print(start)
    print(end)
    return table[start:end][:]

#test. Correct answer for the provided dataset == 44
reducedPatient0 = reduceTableSize(patientTable[0][:][:])
print('%s -> %s'%(patientTable[0][:][:].shape,reducedPatient0.shape))
reducedPatient0.shape = (1,reducedPatient0.shape[0],reducedPatient0.shape[1])
#plotPatients(reducedPatient0,attributeList)

#%%
import numpy as np
from sklearn.preprocessing import Imputer

imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
imp.fit(patientTable[0][:][:])
filledPatient=imp.transform(patientTable[0][:][:])
filledPatient.shape = (1,filledPatient.shape[0],filledPatient.shape[1])
plotPatients(filledPatient,attributeList)


#%% Output results to a file
isWriteToFile = 0
if isWriteToFile:
    f = open('missingDataSinglePatiens.csv','w')
    for attr in attributeList:
        f.write(attr)
        if attr != attributeList[-1]:
            f.write(',')
        
    for i in range(npatients):    
        for j in range(ndays):
            for k in range(nattribs):
                f.write(str(patientTable[i,j,k]))
                if k!=nattribs-1:
                    f.write(',')
            f.write('\n')
            
        #f.write('\n')
    f.close();
            
#%% 
'''from scipy.stats import pearsonr
def getStats(X,y,contrast=np.array([0])):
    B = lstsq(X, y)[0]
    y_hat = X.dot(B)
    MSE = sum((y_hat-y)**2)/X.shape[0]
    
    corr, pvalue = pearsonr(y, y_hat)
    r_squared = corr ** 2
    if contrast.any():
        des_var = contrast.dot(np.linalg.pinv(X.T.dot(X))).dot(contrast.T)
        sse_df = ((y - y_hat) ** 2).sum() / (X.shape[0] - X.shape[1])
        se = np.sqrt(sse_df * des_var)
        t_val = contrast.dot(B) / se

        return y_hat, MSE, r_squared,t_val
    else:
        return y_hat, MSE, r_squared
    
#%% Find the betas for possible correlations
from numpy.linalg import lstsq

Y = patientTable[:,0]
X = patientTable[:,1:]
intercept = np.ones((ndays, 1))
tuple_with_arrays = (intercept, X)
X_with_icept = np.hstack(tuple_with_arrays);
                         
y_hat,MSE, r_squared = getStats(X,Y)

np.savetxt("missing_data_per_patient.csv", patientTable, delimiter=",", fmt='%s', header=attributeList)'''

