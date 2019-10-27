import sys, getopt, helpers
from Data import Data
from FileHandler import createObjectsFromAllFiles, createObjectsFromFile, createExitFile, createExitFixationFile
from StatisticsClass import StatisticsClass
from IDT import calculateIdtAlgorithm
from IVT import calculateIvtAlgorithm
from scipy.optimize import least_squares, minimize
from database import initialize_db, getFromDatabase
from ML import calculateMlAlgorithm
import numpy as np
import matplotlib.pyplot as plt
import time
import logging
from memory_profiler import profile, LogFile

def calibrate(xList, yList):
    i = 1
    ssxArr = []
    ssyArr = []
    X = []
    Y = []
    while i < len(xList):
        X.append([xList[i]**2,xList[i],yList[i]**2,yList[i]])
        Y.append([yList[i]**2,yList[i],xList[i]**2,xList[i]])
        ssxArr.append(xList[0])
        ssyArr.append(yList[0])
        i+=1

    x = np.linalg.lstsq(X,ssxArr, rcond=None)
    y = np.linalg.lstsq(Y,ssyArr, rcond=None)

    i = 1
    retX = []
    retY = []
    while i < len(xList):
        retX.append(x[0][0]*xList[i]**2 + x[0][1]*xList[i] + x[0][2]*yList[i]**2 + x[0][3]*yList[i])
        retY.append(y[0][0]*yList[i]**2 + y[0][1]*yList[i] + y[0][2]*xList[i]**2 + y[0][3]*xList[i])
        i += 1
    
    return retX, retY

def convertPointsToCalibration(pointsList):
    start = time.process_time()
    coordX = []
    coordY = []
    retX = []
    retY = []
    
    for i in pointsList:
        coordX.append(i.CoordX)
        coordY.append(i.CoordY)

    retX, retY = calibrate(coordX, coordY)
    for i, item in enumerate(pointsList):
        if not item.Type == 'SS':
            pointsList[i].CoordX = retX[i-1]
            pointsList[i].CoordY = retY[i-1]
    end = time.process_time()
    return pointsList, end - start

@profile(stream=open('result/' + sys.argv[2] + '-' + sys.argv[3] + '.log','w+'), precision=4)
def main(argv):
    statistics = StatisticsClass()
    if sys.argv[1] == '-h':
        print('How to run file: main.py -i <inputfile> <algorithm>')
    elif sys.argv[1] == '-i':
        coordX = []
        coordY = []
        parsedFile, statistics.ImportAndConvertFileStatistic = createObjectsFromFile(sys.argv[2])
        measurementFixations = []

        if (sys.argv[4] == '-d'):
            statistics.ImportDataToDatabase = initialize_db(parsedFile)
            
        print('Converting file time: %s' % statistics.ImportAndConvertFileStatistic)
        parsedMeasurements = []

        if sys.argv[4] == '-f':
            parsedMeasurements = parsedFile
        elif sys.argv[4] == '-d':
            parsedMeasurements, statistics.ImportAndConvertDatabaseStatistic = getFromDatabase()
        else:
            parsedMeasurements = parsedFile

        if sys.argv[3] == 'I-DT':
            print('Starting measurement using I-DT algorithm')
            for e, measurement in enumerate(parsedMeasurements):
                print('Starting calibration')
                m1, convertingTime = convertPointsToCalibration(measurement)
                statistics.CalibrationSummaryTime += convertingTime
                for i, item in enumerate(m1):
                    if item.Type == 'SS':
                        plt.plot(m1[i].CoordX, m1[i].CoordY, 'ko', markersize=10, label='Eye-tracker points' if i == 0 else "")
                print('Calculating using I-DT point #' + str(e))     
                coordX, coordY, timealgorithm, fixationsForPoint, fixations = calculateIdtAlgorithm(m1)
                statistics.AlgorithmRunTimeStatistic += timealgorithm
                statistics.NumberOfFixationsCount += fixationsForPoint
                measurementFixations.append(fixations)
                plt.plot(coordX, coordY, 'wo', markersize=5, markeredgecolor='r', label='Calculated fixations')
            print('Ending measurement using I-DT algorithm')
            plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            plt.show()
        elif sys.argv[3] == 'I-VT':
            print('Starting measurement using I-VT algorithm')
            for e, measurement in enumerate(parsedMeasurements):
                print('Starting calibration')
                m1, convertingTime = convertPointsToCalibration(measurement)
                statistics.CalibrationSummaryTime += convertingTime
                print('Ended calibration')
                for i, item in enumerate(m1):
                    if item.Type == 'SS':
                        plt.plot(m1[i].CoordX, m1[i].CoordY, 'ko', markersize=10, label='Eye-tracker points' if i == 0 else "")
                print('Calculating using I-VT point #' + str(e))               
                coordX, coordY, timealgorithm, fixationsForPoint, fixations = calculateIvtAlgorithm(m1)
                statistics.AlgorithmRunTimeStatistic += timealgorithm
                statistics.NumberOfFixationsCount += fixationsForPoint
                measurementFixations.append(fixations)
                plt.plot(coordX, coordY, 'wo', markersize=5, markeredgecolor='r', label='Calculated fixations')
            print('Ending measurement using I-VT algorithm')
            plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            plt.show()
        elif sys.argv[3] == 'ML':
            print('Starting measurement using Machine Learning algorithm')
            for measurement in parsedMeasurements:
                m1, convertingTime = convertPointsToCalibration(measurement)
                statistics.CalibrationSummaryTime += convertingTime
                for i, item in enumerate(m1):
                    if item.Type == 'SS':
                        plt.plot(m1[i].CoordX, m1[i].CoordY, 'ko', markersize=10, label='Eye-tracker points')
                calculateMlAlgorithm(m1)
                #plt.plot(coordX, coordY, 'wo', markersize=5, markeredgecolor='r', label='Calculated fixations')
            print('Ending measurement using Machine Learning algorithm')
            #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            #plt.show()
        else:
            print('INCORRECT ALGORITHM')
        print('Number of fixations: %s, Algorithm runtime: %s s' % (statistics.NumberOfFixationsCount, statistics.AlgorithmRunTimeStatistic))
        createExitFile(sys.argv[2], statistics)
        createExitFixationFile(sys.argv[2], measurementFixations)
    elif sys.argv[1] == '-a':
        print('Available algorithms: "I-DT", "I-VT", "ML"')
    else:
        print('How to run file: main.py -i <inputfile> <algorithm>')

if __name__ == "__main__":
    main(sys.argv[:1])
    