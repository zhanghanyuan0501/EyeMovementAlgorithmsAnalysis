import csv, os, datetime, time, StatisticsClass
from Data import Data

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
    start = time.process_time()
    results = []
    for file in os.listdir('./data'):
        if file.endswith(fileName):
            with open('./data/' + file, newline='') as inputfile:
                for line in inputfile:
                    splittedLine = line.strip('\r\n').split('\t')
                    results.append(Data(splittedLine[0], splittedLine[1], splittedLine[2], splittedLine[3]))
    retList = []
    returnList = []
    i = 0
    loopFlag = True
    while loopFlag:
        for element in results:
            if i + 1 == len(results):
                retList.append(results[i])
                loopFlag = False
                break
            if results[i + 1].Type == 'SS':
                retList.append(results[i])
                break
            retList.append(results[i])
            i += 1
        i += 1
        returnList.append(retList)
        retList = []
    end = time.process_time()
    return returnList, '%.3f' % (end - start)

def createExitFile(fileName, statisticClass):
    fieldNames = ['ImportAndConvertFileStatistic',
        'AlgorithmRunTimeStatistic'
        'NumberOfFixationsCount']
    with open('./result/' + fileName + '.csv', 'wb') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerow({
            'ImportAndConvertFileStatistic': str(statisticClass.ImportAndConvertFileStatistic),
            'AlgorithmRunTimeStatistic': str(statisticClass.AlgorithmRunTimeStatistic),
            'NumberOfFixationsCount': str(statisticClass.NumberOfFixationsCount)
        })