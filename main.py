import sys, getopt
from Data import Data
from importFiles import createObjectsFromAllFiles, createObjectsFromFile
from StatisticsClass import StatisticsClass
from IDT import calculateIdtAlgorithm

def main(argv):
    statistics = StatisticsClass()
    if sys.argv[1] == '-h':
        print('How to run file: main.py -i <inputfile> <algorithm>')
    elif sys.argv[1] == '-i':
        parsedFile, statistics.ImportAndConvertFileStatistic = createObjectsFromFile(sys.argv[2])
        print(statistics.ImportAndConvertFileStatistic)
        if sys.argv[3] == 'I-DT':
            calculateIdtAlgorithm(parsedFile)
        elif sys.argv[3] == 'I-VT':
            print('I-VT not implemented yet!')
        else:
            print('INCORRECT ALGORITHM')
    elif sys.argv[1] == '-a':
        print('Available algorithms: "I-DT"')
    else:
        print('How to run file: main.py -i <inputfile> <algorithm>')

if __name__ == "__main__":
    main(sys.argv[:1])
    