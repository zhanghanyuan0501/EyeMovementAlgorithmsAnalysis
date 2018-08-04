import sys, getopt
from Data import Data
from importFiles import createObjectsFromAllFiles, createObjectsFromFile
from StatisticsClass import StatisticsClass

def main(argv):
    statistics = StatisticsClass()
    if sys.argv[1] == '-h':
        print('How to run file: main.py -i <inputfile>')
    elif sys.argv[1] == '-i':
        parsedFile, statistics.ImportAndConvertFileStatistic = createObjectsFromFile(sys.argv[2])
        print(statistics.ImportAndConvertFileStatistic)
    else:
        print('How to run file: main.py -i <inputfile>')

if __name__ == "__main__":
    main(sys.argv[:1])
    