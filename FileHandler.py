import csv, os, datetime, time, StatisticsClass
from Data import Data
import uuid

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
        'CalibrationSummaryTime',
        'AlgorithmRunTimeStatistic',
        'NumberOfFixationsCount',
        'ImportDataToDatabase',
        'ImportAndConvertDatabaseStatistic']
    now = datetime.datetime.now()
    with open('./result/' + fileName + now.strftime("%d-%m-%Y-%H%M%S") + '.csv', 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerow({
            'ImportAndConvertFileStatistic': str(statisticClass.ImportAndConvertFileStatistic),
            'CalibrationSummaryTime': str(statisticClass.CalibrationSummaryTime),
            'AlgorithmRunTimeStatistic': str(statisticClass.AlgorithmRunTimeStatistic),
            'NumberOfFixationsCount': str(statisticClass.NumberOfFixationsCount),
            'ImportDataToDatabase': str(statisticClass.ImportDataToDatabase),
            'ImportAndConvertDatabaseStatistic': str(statisticClass.ImportAndConvertDatabaseStatistic)
        })

def createExitFixationFile(fileName, data):
    fieldNames = ['CoordX',
        'CoordY',
        'TimeStamp']
    now = datetime.datetime.now()
    with open('./result/fixation_' + fileName + now.strftime("%d-%m-%Y-%H%M%S") + '.csv', 'w', newline='') as csvFile:
        writer = csv.DictWriter(csvFile, fieldnames=fieldNames)
        writer.writeheader()
        for list in data:
            for item in list:
                writer.writerow({
                    'CoordX': str(item.CoordX),
                    'CoordY': str(item.CoordY),
                    'TimeStamp': str(item.TimeStamp)
                })