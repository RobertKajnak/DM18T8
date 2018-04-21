from helperFunctions import plotPatient
from getDataset import getDataset


#def main():
''' dataset == a list of patient talbes, i.e.:
 nr_patients x [nr_days_for_that_patient x nr_of_attributes]
 more precisely: 23 x [days(varies) x 40]
 nr_patients is a list
 [nr_days_for_that_patient x nr_of_attributes] should be and n-d-python array
 
 attrubiteList == list of the attributes for the columns, i.e.:
 ['mood','mood_count',...,'sleep','nightlife']'''
[dataset,attributeList] = getDataset()


'''First parameter is the patient to be plotted, second is the titles for the
graphs i.e. the attribute names'''
plotPatient(dataset[0],attributeList)

#if __name__ == '__main__':
#  main()
