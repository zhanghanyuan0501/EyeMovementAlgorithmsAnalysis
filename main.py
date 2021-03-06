import sys, getopt, helpers
from Data import Data
from FileHandler import createObjectsFromAllFiles, createObjectsFromFile, createExitFile, createExitFixationFile
from StatisticsClass import StatisticsClass
import IVT as ivt
import IDT as idt
from scipy.optimize import least_squares, minimize
from database import initialize_db, getFromDatabase
import ML as ml
import numpy as np
import matplotlib.pyplot as plt
import time
import logging
from memory_profiler import profile, LogFile

def calibrate(xList, yList):
    i = 0
    ssxArr = []
    ssyArr = []
    tmpX = np.asarray(xList)
    tmpY = np.asarray(yList)
    # X = []
    # Y = []
    while i < len(xList):
        # X.append([xList[i]**2,xList[i],yList[i]**2,yList[i]])
        # Y.append([yList[i]**2,yList[i],xList[i]**2,xList[i]])
        ssxArr.append(xList[0])
        ssyArr.append(yList[0])

        i+=1

    ssxTmp = np.asarray(ssxArr)
    ssyTmp = np.asarray(ssyArr)
    temp = np.polynomial.Polynomial.fit(tmpX, tmpY, 2)
    x_fit = np.polynomial.Polynomial(temp)
    x_test = x_fit(ssxTmp[1:])[0]
    tempY = np.polynomial.Polynomial.fit(tmpY, tmpX, 2)
    y_fit = np.polynomial.Polynomial(tempY)
    y_test = y_fit(ssyTmp[1:])[0]
    retX = x_test(tmpX[1:])
    retY = y_test(tmpY[1:])
    # x = np.linalg.lstsq(X,ssxArr, rcond=None)
    # y = np.linalg.lstsq(Y,ssyArr, rcond=None)

    i = 1
    # retX = []
    # retY = []
    # while i < len(xList):
    #     retX.append(x[0][0]*xList[i]**2 + x[0][1]*xList[i] + x[0][2]*yList[i]**2 + x[0][3]*yList[i])
    #     retY.append(y[0][0]*yList[i]**2 + y[0][1]*yList[i] + y[0][2]*xList[i]**2 + y[0][3]*xList[i])
    #     i += 1
    
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
    print(retX)
    for i, item in enumerate(pointsList):
        if not item.Type == 'SS':
            pointsList[i].CoordX = retX[i-1]
            pointsList[i].CoordY = retY[i-1]
    end = time.process_time()
    return pointsList, end - start

@profile(stream=open('result/' + sys.argv[2] + '-' + sys.argv[3] + '.log','w+'), precision=10)
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
                for i, item in enumerate(measurement):
                    if item.Type == 'SS':
                        plt.plot(item.CoordX, item.CoordY, 'ko', markersize=10, label='Eye-tracker points' if i == 0 else "")
                print('Calculating using I-DT point #' + str(e))     
                coordX, coordY, timealgorithm, fixationsForPoint, fixations, saccade = idt.calculateIdtAlgorithm(measurement)
                statistics.AlgorithmRunTimeStatistic += timealgorithm
                statistics.NumberOfFixationsCount += fixationsForPoint
                statistics.SaccadeCount += saccade
                measurementFixations.append(fixations)
                plt.plot(coordX, coordY, 'wo', markersize=5, markeredgecolor='r', label='Calculated fixations')
            print('Ending measurement using I-DT algorithm')
            plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            
        elif sys.argv[3] == 'I-VT':
            print('Starting measurement using I-VT algorithm')
            for e, measurement in enumerate(parsedMeasurements):
                for i, item in enumerate(measurement):
                    if item.Type == 'SS':
                        plt.plot(item.CoordX, item.CoordY, 'ko', markersize=10, label='Eye-tracker points' if i == 0 else "")
                print('Calculating using I-VT point #' + str(e))               
                coordX, coordY, timealgorithm, fixationsForPoint, fixations, saccades = ivt.calculateIvtAlgorithm(measurement)
                statistics.SaccadeCount += len(saccades)
                statistics.AlgorithmRunTimeStatistic += timealgorithm
                statistics.NumberOfFixationsCount += fixationsForPoint
                measurementFixations.append(fixations)
                saccades = np.asarray(saccades)
                tmpX = []
                tmpY = []
                for i in saccades:
                    tmpX.append(i.CoordX)
                    tmpY.append(i.CoordY)
                #plt.plot(tmpX, tmpY, 'wo', markersize=2, markeredgecolor='g')
                plt.plot(coordX, coordY, 'wo', markersize=5, markeredgecolor='r', label='Calculated fixations')
            print('Ending measurement using I-VT algorithm')
            plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            
        elif sys.argv[3] == 'ML':
            print('Starting measurement using Machine Learning algorithm')
            convertedData = []
            allFixations = []
            for measurement in parsedMeasurements:
                for i, item in enumerate(measurement):
                    if item.Type == 'SS':
                        plt.plot(item.CoordX, item.CoordY, 'ko', markersize=10, label='Eye-tracker points' if i == 0 else "")
                fixations = ivt.prepareDataIvt(measurement)
                allFixations.extend(fixations)
                convertedData.append(measurement)

            points = []
            for i, item in enumerate(convertedData): 
                mlHelperArray = ml.calculateMlHelper(item, allFixations)
                points.append(mlHelperArray)
            coordX, coordY, fixationsForPoint, timealgorithm, ite, measurementFixations, saccadeCount = ml.calculateML(points)
            plt.plot(coordX, coordY, 'wo', markersize=5, markeredgecolor='r', label='Calculated fixations')
            statistics.NumberOfFixationsCount += fixationsForPoint
            statistics.AlgorithmRunTimeStatistic += timealgorithm
            statistics.MLPrecision = ite
            statistics.SaccadeCount = saccadeCount
            print('Ending measurement using Machine Learning algorithm')
            plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            
        else:
            print('INCORRECT ALGORITHM')
        print('Number of fixations: %s, Algorithm runtime: %s s, Saccades %s' % (statistics.NumberOfFixationsCount, statistics.AlgorithmRunTimeStatistic, statistics.SaccadeCount))
        fig1 = plt.gcf()
        #plt.show()
        plt.draw()
        fig1.savefig('result/' + sys.argv[2] + sys.argv[3] + '.png', dpi=100)
        createExitFile(sys.argv[2], statistics, sys.argv[3])
        createExitFixationFile(sys.argv[2], measurementFixations, sys.argv[3])
    elif sys.argv[1] == '-a':
        print('Available algorithms: "I-DT", "I-VT", "ML"')
    else:
        print('How to run file: main.py -i <inputfile> <algorithm>')

if __name__ == "__main__":
    main(sys.argv[:1])
    