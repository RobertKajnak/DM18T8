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
from datetime import date as dt
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
        
        for attrib in patients[patient][day]:
            S=0.0
            countDays=0.0
            for time in patients[patient][day][attrib]:
                S+=patients[patient][day][attrib][time]
                countDays+=1;
            patients[patient][day][attrib] = S/countDays
            
    #ndays-=nregr;
    ndays=max(ndays,ndaysprev)
            
#%% Convert into a table optimized for statistical analysis
# All the computational advantages mentioned in section 1 are now removed by
# converting it into a table, but is (to be seen) easier to code for statistical
# analysis
            

#NOTE: next(iter(patients.values())) can be used ot access first element
target = 'mood'
nattribs = 19
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
 'appCat.weather']

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
        
#%%
'''
for patient in patients:
    attribs = list(patients[patient].keys())
    indT = attribs.index(target)
    #swap the target witht the first element
    attribs[0],attribs[indT] = attribs[indT],attribs[0]
    attribs[1:] = sorted(attribs[1:])
    for indA,attrib in enumerate(attribs):
        avgs=[]
        
        #print(indD)
        indD=-nregr;
        for i,day in enumerate(patients[patient][attrib]):
            j= min(i,nregr)
                
            if attrib==target:
                if indD>=0:
                    patientTable[indD][indA] = patients[patient][attrib][day]
            else:
                avgs.insert(0, patients[patient][attrib][day])
                #we want the avg to be 1 less than the index of the target
                if len(avgs)>=nregr:
                    avgs.pop(-1)
                    patientTable[indD][indA] = np.mean(avgs)
            indD+=1;
'''
#%% plot two of the attributes to see visually check results

import matplotlib.pyplot as plt

f = open('missingDataSinglePatiens.csv','w')
for attr in attributeList:
    f.write(attr)
    if attr != attributeList[-1]:
        f.write(',')
    
for i in range(4):
    print('Patient %d'%i)
    plt.figure(figsize=(12,10))
    for j in range(nattribs):
        plt.subplot(5,4,j+1)
        plt.scatter(range(len(patientTable[i,:,j])),patientTable[i,:,j])
        plt.title(attributeList[j])
        plt.ylabel('Mean Value')
        plt.xlabel('Time')
    
    for j in range(ndays):
        for k in range(nattribs):
            f.write(str(patientTable[i,j,k]))
            if k!=nattribs-1:
                f.write(',')
        f.write('\n')
        
    #f.write('\n')
    plt.tight_layout()
    plt.show()
f.close();
#screen time should matter
#plt.plot(patientTable[:,-2])
            
#%% 
from scipy.stats import pearsonr
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

np.savetxt("missing_data_per_patient.csv", patientTable, delimiter=",", fmt='%s', header=attributeList)

