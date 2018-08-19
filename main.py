import sys, getopt, helpers
from Data import Data
from FileHandler import createObjectsFromAllFiles, createObjectsFromFile, createExitFile
from StatisticsClass import StatisticsClass
from IDT import calculateIdtAlgorithm
from IVT import calculateIvtAlgorithm
from ML import calculateMlAlgorithm

def main(argv):
    statistics = StatisticsClass()
    if sys.argv[1] == '-h':
        print('How to run file: main.py -i <inputfile> <algorithm>')
    elif sys.argv[1] == '-i':
        coordX = []
        coordY = []
        parsedFile, statistics.ImportAndConvertFileStatistic = createObjectsFromFile(sys.argv[2])
        print('Converting file time: %s' % statistics.ImportAndConvertFileStatistic)
        if sys.argv[3] == 'I-DT':
            for measurement in parsedFile:
                coordX, coordY, statistics.AlgorithmRunTimeStatistic, statistics.NumberOfFixationsCount = calculateIdtAlgorithm(measurement)
                helpers.plotResults(coordX, coordY, sys.argv[3])
        elif sys.argv[3] == 'I-VT':
            calculateIvtAlgorithm(parsedFile)
        elif sys.argv[3] == 'ML':
            calculateMlAlgorithm(parsedFile)
        else:
            print('INCORRECT ALGORITHM')
        print('Number of fixations: %s, Algorithm runtime: %s' % (statistics.NumberOfFixationsCount, statistics.AlgorithmRunTimeStatistic))
        createExitFile(sys.argv[2], statistics)
    elif sys.argv[1] == '-a':
        print('Available algorithms: "I-DT", "I-VT", "ML"')
    else:
        print('How to run file: main.py -i <inputfile> <algorithm>')

if __name__ == "__main__":
    main(sys.argv[:1])
    