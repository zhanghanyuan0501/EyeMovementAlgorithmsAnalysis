import csv, os, datetime, sys, getopt
from time import mktime
from Data import Data

def convertToReadableDate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1e3).strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]

# Create array of Data from Data files
def createObjectsFromAllFiles():
    results = []
    for file in os.listdir('./data'):
        if file.endswith('.cal'):
            with open('./data/' + file, newline='') as inputfile:
                for line in inputfile:
                    splittedLine = line.strip('\r\n').split('\t')
                    results.append(Data(splittedLine[0], convertToReadableDate(int(splittedLine[1])), splittedLine[2], splittedLine[3]))
    return results

def createObjectsFromFile(fileName):
    results = []
    for file in os.listdir('./data'):
        if file.endswith(fileName):
            with open('./data/' + file, newline='') as inputfile:
                for line in inputfile:
                    splittedLine = line.strip('\r\n').split('\t')
                    results.append(Data(splittedLine[0], convertToReadableDate(int(splittedLine[1])), splittedLine[2], splittedLine[3]))
    return results

def main(argv):
    parsedFile = []

    if sys.argv[1] == '-h':
        print('How to run file: main.py -i <inputfile>')
    elif sys.argv[1] == '-i':
        parsedFile = createObjectsFromFile(sys.argv[2])
    else:
        print('How to run file: main.py -i <inputfile>')
    
    print(parsedFile[0].TimeStamp)

if __name__ == "__main__":
    main(sys.argv[:1])
    