import constants, time
from helpers import convertToReadableDate

def calculateIdtAlgorithm(pointsList):
    start = time.process_time()
    i = 0
    timeStart = int(pointsList[0].TimeStamp)
    windowList = []
    coordXList = []
    coordYList = []
    try:
        while(i < len(pointsList)):
            if (pointsList[i].Type == 'SS'):
                print(pointsList[i].Type)
                i += 1
                continue
            currTime = int(pointsList[i].TimeStamp)
            if (currTime - timeStart <= constants.WINDOW_THRESHOLD):
                windowList.append(pointsList[i])
                Dispersion = (max(maxX.CoordX for maxX in windowList) - min(minX.CoordX for minX in windowList)) + (max(maxY.CoordY for maxY in windowList) - min(minY.CoordY for minY in windowList))
                if Dispersion > constants.DISPERSION_THRESHOLD and len(windowList) > 1:
                    coordXList.append(sum(sumX.CoordX for sumX in windowList) / len(windowList))
                    coordYList.append(sum(sumY.CoordY for sumY in windowList) / len(windowList))
            else:
                timeStart = currTime
                windowList = []
            i += 1
        end = time.process_time()
        return coordXList, coordYList, '%.3f' % (end - start), len(coordXList)
    except Exception as e:
        print('exception %s' % e)
