#%% plot two of the attributes to see visually check results
import matplotlib.pyplot as plt
import numpy as np
def writeTableToCSV234(filename,table,attributeList):
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

