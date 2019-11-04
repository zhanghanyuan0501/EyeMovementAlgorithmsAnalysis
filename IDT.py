import constants, time
from helpers import convertToReadableDate
from memory_profiler import profile, LogFile

def calculateIdtAlgorithm(pointsList):
    start = time.process_time()
    i = 0
    timeStart = int(pointsList[0].TimeStamp)
    windowList = []
    coordXList = []
    coordYList = []
    retList = []
    countPoints = len(pointsList)
    while i < countPoints - 1:
        if pointsList[i].Type == 'SS':
            i += 1
            continue
        currTime = int(pointsList[i].TimeStamp)
        while currTime - timeStart <= constants.WINDOW_TIME_THRESHOLD:
            windowList.append(pointsList[i])
            i += 1
            if i >= countPoints:
                break
            currTime = int(pointsList[i].TimeStamp)
        if i >= countPoints:
            break
        if len(windowList) > 1:
            Dispersion = (max(maxX.CoordX for maxX in windowList) - min(minX.CoordX for minX in windowList)) + (max(maxY.CoordY for maxY in windowList) - min(minY.CoordY for minY in windowList))
        while len(windowList) > 1:
            if Dispersion <= constants.DISPERSION_THRESHOLD and len(windowList) > 1:
                while (Dispersion < constants.DISPERSION_THRESHOLD):
                    windowList.append(pointsList[i])
                    i += 1
                    if i >= countPoints:
                        break
                    Dispersion = (max(maxX.CoordX for maxX in windowList) - min(minX.CoordX for minX in windowList)) + (max(maxY.CoordY for maxY in windowList) - min(minY.CoordY for minY in windowList))
                if i >= countPoints:
                    break
                retList.extend(windowList)
                coordXList.append(sum(sumX.CoordX for sumX in windowList) / len(windowList))
                coordYList.append(sum(sumY.CoordY for sumY in windowList) / len(windowList))
                windowList = []
            else:
                windowList.pop(0)
        if i <= countPoints - 1:
            timeStart = int(pointsList[i].TimeStamp)
    end = time.process_time()
    return coordXList, coordYList, end - start, len(coordXList), retList, (countPoints - len(retList))