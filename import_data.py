import csv, os, datetime
from time import mktime
from Data import Data

def convertToReadableDate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1e3).strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]

# Create array of Data from Data files
results = []
for file in os.listdir('./data'):
    if file.endswith('.cal'):
        with open('./data/' + file, newline='') as inputfile:
            for line in inputfile:
                splittedLine = line.strip('\r\n').split('\t')
                results.append(Data(splittedLine[0], convertToReadableDate(int(splittedLine[1])), splittedLine[2], splittedLine[3]))