from helperFunctions import plotPatient
from getDataset import getDataset


def main():
    [dataset,attributeList] = getDataset()
    plotPatient(dataset[0],attributeList)

if __name__ == '__main__':
  main()
