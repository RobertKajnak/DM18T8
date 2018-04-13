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
        except:
            #if invalid value is detected e.g. NA, it skips that value
            continue;
        #The algorithm tries to access the dictionary field.
        #If it fails, it attempts to create the last field.
        #if that fails, it attempts to create the previous one, and so on
        try:
            patients[id] [attr] [date] [time] = val 
        except:
            try:
                patients[id] [attr] [date] = {}
                patients[id] [attr] [date] [time]  = val
            except:
                try:
                    patients[id] [attr] = {}
                    patients[id] [attr] [date] = {}
                    patients[id] [attr] [date] [time]= val
                except:
                    patients[id] = {}
                    patients[id] [attr]={}
                    patients[id] [attr] [date] ={ }
                    patients[id] [attr] [date] [time] = val
                    
        k+=1
        #if k>6000:
        #    break;
            
#%% Create average for days and reallocate as such

#var for next section
ndays = 0;
nregr=5;

for patient in patients:
    for attrib in patients[patient]:
        ndaysprev=ndays;
        ndays=0;
        
        for day in patients[patient][attrib]:
            S=0.0
            c=0.0
            ndays+=1
            for time in patients[patient][attrib][day]:
                S+=patients[patient][attrib][day][time]
                c+=1;
            patients[patient][attrib][day] = S/c
            
        ndays-=nregr;
        ndays=max(ndays,ndaysprev)
            
#%% Convert into a table optimized for statistical analysis
# All the computational advantages mentioned in section 1 are now removed by
# converting it into a table, but is (to be seen) easier to code for statistical
# analysis
            
#NOTE: next(iter(patients.values())) can be used ot access first element
target = 'mood'
nattribs = len(next(iter(patients.values())).keys())
patientTable = np.zeros([ndays,nattribs])
indD=0;

for patient in patients:
    attribs = list(patients[patient].keys())
    indT = attribs.index(target)
    #swap the target witht the first element
    attribs[0],attribs[indT] = attribs[indT],attribs[0]
    attribs[1:] = sorted(attribs[1:])
    for indA,attrib in enumerate(attribs):
        avgs=[]
        
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

#%% plot two of the attributes to see visually check results
print('The order of the columns is:')
print(attribs)
import matplotlib.pyplot as plt

plt.subplot(2,1,1)
plt.plot(patientTable[:,0])
plt.subplot(2,1,2)
#screen time should matter
plt.plot(patientTable[:,-2])
            
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

