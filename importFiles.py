import csv, os, datetime
from Data import Data
import timeit

# Create array of Data from Data files
def createObjectsFromAllFiles():
    results = []
    for file in os.listdir('./data'):
        if file.endswith('.cal'):
            with open('./data/' + file, newline='') as inputfile:
                for line in inputfile:
                    splittedLine = line.strip('\r\n').split('\t')
                    results.append(Data(splittedLine[0], splittedLine[1], splittedLine[2], splittedLine[3]))
    return results

def createObjectsFromFile(fileName):
    start = timeit.default_timer()
    results = []
    for file in os.listdir('./data'):
        if file.endswith(fileName):
            with open('./data/' + file, newline='') as inputfile:
                for line in inputfile:
                    splittedLine = line.strip('\r\n').split('\t')
                    results.append(Data(splittedLine[0], splittedLine[1], splittedLine[2], splittedLine[3]))
    end = timeit.default_timer()
    return results, '%.3f' % (end - start)
