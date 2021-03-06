from helperFunctions import plotPatient
from helperFunctions import writePatientToCSV
from getDataset import getNormalizedDataset


#def main():
''' dataset == a list of patient talbes, i.e.:
 nr_patients x [nr_days_for_that_patient x nr_of_attributes]
 more precisely: 23 x [days(varies) x 40]
 nr_patients is a list
 [nr_days_for_that_patient x nr_of_attributes] should be and n-d-python array
 
 attrubiteList == list of the attributes for the columns, i.e.:
 ['mood','mood_count',...,'sleep','nightlife']'''
[dataset,attributeList] = getNormalizedDataset()


'''First parameter is the patient to be plotted, second is the titles for the
graphs i.e. the attribute names'''
plotPatient(dataset[1],attributeList)

'''To save an individual patient to a  file specify the filename, the patient 
and the attribute list returned above'''
#writePatientToCSV('patient1.csv',dataset[1],attributeList)

'''To export all the patient data uncomment the lines below'''
import os
if not os.path.exists('patientData'):
    os.makedirs('patientData')
for i,patient in enumerate(dataset):
    writePatientToCSV('patientData/patient%d.csv'%i,patient,attributeList)

#if __name__ == '__main__':
#  main()
