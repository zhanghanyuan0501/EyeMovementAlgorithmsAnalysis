import time, Data, math, constants, sys
from memory_profiler import profile, LogFile

def calculateIvtAlgorithm(pointList):
    start = time.process_time()
    fixations = []
    coordX = []
    coordY = []
    i = 0
    for element in pointList:
        velocity = 0
        if pointList[i].Type == 'SS':
            i += 1
            continue
        if i + 1 == len(pointList) - 1:
            velocity = math.sqrt(math.pow(pointList[i + 1].CoordX - pointList[i].CoordX, 2) + math.pow(pointList[i + 1].CoordY - pointList[i].CoordY, 2))
            if velocity < constants.FIXATION_VELOCITY_THRESHOLD:
                fixations.append(pointList[i])
                fixations.append(pointList[i + 1])
            break
        velocity = math.sqrt(math.pow(pointList[i + 1].CoordX - pointList[i].CoordX, 2) + math.pow(pointList[i + 1].CoordY - pointList[i].CoordY, 2))

        if (velocity < constants.FIXATION_VELOCITY_THRESHOLD):
            fixations.append(pointList[i])
        i += 1
    
    i = 0
    combineFixationsArray = []
    while i < len(fixations) - 1:
        velocity = math.sqrt(math.pow(fixations[i + 1].CoordX - fixations[i].CoordX, 2) + math.pow(fixations[i + 1].CoordY - fixations[i].CoordY, 2))
        if velocity < constants.FIXATION_VELOCITY_THRESHOLD:
            combineFixationsArray.append(fixations[i])
        else:
            if len(combineFixationsArray) != 0:
                coordX.append(sum(sumX.CoordX for sumX in combineFixationsArray) / len(combineFixationsArray))
                coordY.append(sum(sumY.CoordY for sumY in combineFixationsArray) / len(combineFixationsArray))

        i += 1

        
    end = time.process_time()
    return coordX, coordY, end - start, len(coordX), fixations