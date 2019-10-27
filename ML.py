import constants
from operator import attrgetter
from math import sqrt
from Data import Data

###
#prędkość pomiędzy każdymi dwoma punktami,
#- odległości pomiędzy każdymi dwoma punktami (x1-x2) + (y1-y2) 
#- odległości (xmax-xmin) + (ymax-ymin) w całym oknie
#- średnią prędkość w całym oknie,
#- odchylenie standardowe w oknie zarówno dla prędkości jak i odległości między punktami.
###



### PYTANIA:
# - czy najpierw dodać wszystko do okna i potem zacząć obliczanie wszystkich pól
##
class MLHelper:
    def __init__(self, Type, CoordX, CoordY, TimeStamp,  *args, **kwargs):
        self.Data = Data(Type, TimeStamp, CoordX, CoordY)
        self.VelocityBetweenPoints = float(0)
        self.DistancesBetweenPoints = float(0)
        self.DistancesWindow = float(0)
        self.AverageVelocityInWindow = float(0)
        self.DeviationWindowVelocity = float(0)
        self.DeviationWindowDistances = float(0)

def calculateMlAlgorithm(pointList):
    tempArr = []
    i = 0
    helperArr = []
    while i < len(pointList):
        helper = MLHelper(pointList[i].Type, pointList[i].CoordX, pointList[i].CoordY, pointList[i].TimeStamp)
        if (len(pointList) == i + 1):
            break
        if (len(tempArr) == 0 or (int(pointList[i + 1].TimeStamp) - int(tempArr[0].TimeStamp) < constants.WINDOW_MACHINE_LEARNING_TIME_THRESHOLD)):
            tempArr.append(pointList[i])
        else:
            Xmin = min(tempArr, key=attrgetter('CoordX'))
            Ymin = min(tempArr, key=attrgetter('CoordY'))
            Xmax = max(tempArr, key=attrgetter('CoordX'))
            Ymax = max(tempArr, key=attrgetter('CoordY'))
            helper.DistancesWindow = (Xmax.CoordX - Xmin.CoordX) + (Ymax.CoordY - Ymin.CoordY)
            if (len(tempArr) > 0):
                prevMeasurement = tempArr[len(tempArr) - 1]
                timeDiff = int(pointList[i].TimeStamp) - int(prevMeasurement.TimeStamp)
                helper.DistancesBetweenPoints = sqrt(pow((prevMeasurement.CoordX + pointList[i].CoordX), 2) + pow((prevMeasurement.CoordY + pointList[i].CoordY), 2))
                if (timeDiff != 0):
                    helper.VelocityBetweenPoints = (helper.DistancesBetweenPoints / timeDiff)
            print(helper.DistancesWindow, helper.DistancesBetweenPoints, helper.VelocityBetweenPoints)
            helperArr.append(helper)            
            tempArr = []
        i += 1
    print('Helper array count:', len(helperArr))

            
        

