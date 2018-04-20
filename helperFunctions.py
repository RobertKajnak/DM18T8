#%% plot two of the attributes to see visually check results
import matplotlib.pyplot as plt
import numpy as np
def writeTableToCSV(filename,table,attributeList):
    [npatients,ndays,nattribs] = table.shape
    
    f = open(filename,'w')
    for attr in attributeList:
        f.write(attr)
        if attr != attributeList[-1]:
            f.write(',')
        
    for i in range(npatients):    
        for j in range(ndays):
            for k in range(nattribs):
                f.write(str(table[i,j,k]))
                if k!=nattribs-1:
                    f.write(',')
            f.write('\n')
            
        #f.write('\n')
    f.close();
    return

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

def plotPatient(patient,attributeList):
    nattribs=patient.shape[1]
    plt.figure(figsize=(14,25))
    for j in range(nattribs):
            plt.subplot(np.ceil(nattribs/3),3,j+1)
            plt.plot(range(len(patient[:,j])),patient[:,j])
            plt.title(attributeList[j])
            plt.ylabel('Mean Value')
            plt.xlabel('Time')
    
    plt.tight_layout()
    plt.show()
    return
        
def reduceTableSize(table,maxNanCount=.35,entryLimit = 3):
    height = table.shape[0]
    width = table.shape[1]
    def isAcceptable(i):
        #print(np.count_nonzero(np.isnan(table[i-entryLimit:i])))
        return np.count_nonzero(np.isnan(table[i]))<=width*maxNanCount
    
    start = height
    prev = []   
    for i in range(entryLimit):
        prev.append(isAcceptable(i))
    
    #deque may provide slightly better performance, but the amount of days does not\
    #warrant the additional readablility hindrance
    for i in range(entryLimit,height):
        prev.pop(0)
        prev.append(isAcceptable(i))
        #check if more than 30% of the data is missing fromt he last entryLimit rows
        #if not that much data missing, the true array starts from there
        if prev.count(True)==entryLimit:
            start = i-3
            break;
    
    end = 0;
    prev = []
    for i in range(height-1,height-entryLimit-1,-1):
        prev.append(isAcceptable(i))  
    for i in reversed(range(height-entryLimit)):
        prev.pop(0)
        prev.append(isAcceptable(i))
        if (i<=start):
            end = start
            break;
        if prev.count(True)==entryLimit:
            end = i+4
            break;
            
    #print('Considering indices %d->%d, total of %d'%(start,end,end-start))
    return table[start:end][:]

