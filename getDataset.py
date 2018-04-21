import csv;
import numpy as np;

def getDataset():
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
    #also add additional variables
    from datetime import datetime
    #var for next section
    ndays = 0;
    
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
    #indD=0;
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
    
    
    #%% Visually check the elements of the table
    #from helperFunctions import plotPatients 
    #plotPatients(patientTable[:1][:][:],attributeList)
    #%% Reduce the table sizes by removing rows from the end and the beginning,
    # that have less than 65% of measurements
    from helperFunctions import reduceTableSize
    #test. Correct answer for the provided dataset == 44
    patientsTrimmed = []
    for i in range(npatients):
        #print ('patient %d data:'%i)
        reducedPatient = reduceTableSize(patientTable[i][:][:],entryLimit=3,maxNanCount=.4)        
        
        if reducedPatient.shape[0]>=25:
            patientsTrimmed.append(reducedPatient)
        '''uncomment following lines to see which patients did not make it'''
        #else:
        #    print(i)
    
    #%% preporcessing the RAW data -- removing 4sigma outliers,
    #filling in missing values with means, adding 0 if the whole attribute is epty    
    patientsEstimated = []
    for patient in patientsTrimmed:
        #calculate variance
        #parse patient column by column. filter out the nan values within colum. 
        #Calculate std from the remaining values
        stds = [np.std(list(filter(lambda x : not np.isnan(x) , a))) for a in patient.transpose()]
        means = [np.mean(list(filter(lambda x : not np.isnan(x) , a))) for a in patient.transpose()]
    
        patientNoOutliers = \
                np.array(list(list(map(lambda x: means[i]-3*stds[i] if x<means[i]-3*stds[i] else \
                      means[i]+3*stds[i] if x>means[i]+3*stds[i] else x,row)) \
                        for i,row in enumerate(patient.T))).T
    
        meansNew = [np.mean(list(filter(lambda x : not np.isnan(x) , a))) for a in patientNoOutliers.T]
        meansNew = [0.0 if np.isnan(mean) else mean for mean in meansNew]
    
        patientsFilled = np.array(list(list(map(lambda x: meansNew[i] if np.isnan(x) else x,row)) \
                              for i,row in enumerate(patientNoOutliers.T))).T
                                    
        patientsEstimated.append(patientsFilled)
    return patientsEstimated,attributeList

def getNormalizedDataset():

    [patientsFilled,attributeList ] = getDataset()
    #%%construct the new attribute List. Constructing it in the for loop with variables
    #  would require adding extra flags and checks
    attributeListNew = []
    skip = ['mood_count','call_count','sms_count','circumplex.arousal_count','circumplex.valence_count','activity_count']
    for attribute in attributeList:
        if  attribute in skip:
            continue;
        if 'count' in attribute:
            attributeListNew.append('%s_avg'%attribute[:-6])
        else:
            attributeListNew.append(attribute);
            
    #%% Cut the values from before, calculate avarages and normalize where necessary
    patientsNormalized = [] 
    for patient in patientsFilled:
        #remove sum of mood and replace wih mood
        normVal=[];
        #Skipping mood, mood_count
        for i in range(patient.T.shape[0]):
            name = attributeList[i]
            skip = ['mood','call_count', 'sms_count','circumplex.valence', 'circumplex.arousal','activity']
            if name in skip :
                continue;
            
            if 'count' in name:
                val = np.divide(patient.T[i-1],patient.T[i])
                #if the second column contains 0s the first one will be NaN. 
                #These are replaced with 0. (0 measurements means a mean of 0)
                val = np.array(list(map(lambda x: 0.0 if np.isnan(x) else x,val)))
            else:
                val = patient.T[i]
            
            #actual normalization
            if name == 'mood_count':
                val = (val-1)/9
            if 'circumplex' in name:
                val = (val+2)/4;
            
            normVal.append(val)
        
        patientsNormalized.append(np.array(normVal).T)
        
    return patientsNormalized,attributeListNew





