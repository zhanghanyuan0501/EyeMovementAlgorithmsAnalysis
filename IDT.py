import constants

def calculateIdtAlgorithm(pointList):
    i = 0
    analyzedPointList = pointList
    while(i < len(analyzedPointList)):
        time = int(analyzedPointList[i].TimeStamp)
        timeStart = int(analyzedPointList[0].TimeStamp)
        if (time - timeStart <= constants.WINDOW_THRESHOLD):
            print(time)
        else:
            timeStart = time
        i += 1