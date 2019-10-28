import constants
from operator import attrgetter
from math import sqrt
from Data import Data
import IVT as ivt

# Load libraries
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import numpy as np
import time
import statistics as st
###
#prędkość pomiędzy każdymi dwoma punktami,
#- odległości pomiędzy każdymi dwoma punktami (x1-x2) + (y1-y2) 
#- odległości (xmax-xmin) + (ymax-ymin) w całym oknie
#- średnią prędkość w całym oknie,
#- odchylenie standardowe w oknie zarówno dla prędkości jak i odległości między punktami.
###


class MLHelper:
    def __init__(self, Type, CoordX, CoordY, TimeStamp,  *args, **kwargs):
        self.Data = Data(Type, TimeStamp, CoordX, CoordY)
        self.VelocityBetweenPoints = float(0)
        self.DistancesBetweenPoints = float(0)
        # self.DistancesWindow = float(0)
        # self.AverageVelocityInWindow = float(0)
        # self.DeviationWindowVelocity = float(0)
        # self.DeviationWindowDistances = float(0)
        self.IsFixation = bool

    def __iter__(self):
        yield 'Data', self.Data
        yield 'VEL', self.VelocityBetweenPoints
        yield 'DBP', self.DistancesBetweenPoints
        # yield 'DW', self.DistancesWindow
        # yield 'AVIW', self.AverageVelocityInWindow
        # yield 'DWV', self.DeviationWindowVelocity
        # yield 'DWD', self.DeviationWindowDistances
        yield 'FIX', 1 if self.IsFixation == True else 0


def calculateMlHelper(pointList, existingFixations):
    i = 0
    while i < len(pointList):
        windowTime = int(0)
        j = i + 1
        helperArr = []
        helper2 = []
        helper2.append(pointList[i])
        helper = MLHelper(pointList[i].Type, pointList[i].CoordX, pointList[i].CoordY, pointList[i].TimeStamp)
        helper.IsFixation = pointList[i] in existingFixations
        if i + 1 < len(pointList):
            helper.VelocityBetweenPoints = ivt.calculateVelocitiesBetweenPoints(pointList[i], pointList[i + 1])
            helper.DistancesBetweenPoints = (pointList[i].CoordX - pointList[i+1].CoordX) + (pointList[i].CoordY - pointList[i + 1].CoordY)

        # while windowTime <= constants.WINDOW_TIME_THRESHOLD:
        #     if (j < len(pointList)):
        #         windowTime = int(pointList[j].TimeStamp) - int(pointList[i].TimeStamp)
        #         helper2.append(pointList[j])
        #         j += 1
        #     else:
        #         break
        
        # helper.DistancesWindow = (max(x.CoordX for x in helper2) - min(x.CoordX for x in helper2)) + (max(x.CoordY for x in helper2) - min(x.CoordY for x in helper2)) if len(helper2) > 0 else 0
        # velArr = []
        # distArr = []
        # for e, item in enumerate(helper2):
        #     if e + 1 < len(helper2):
        #         velArr.append(ivt.calculateVelocitiesBetweenPoints(helper2[e], helper2[e+1]))
        #         distArr.append((helper2[e].CoordX - helper2[e+1].CoordX) + (helper2[e].CoordY - helper2[e + 1].CoordY))

        # helper.AverageVelocityInWindow = st.mean(velArr) if len(velArr) > 1 else 0
        # helper.DeviationWindowVelocity = st.stdev(velArr) if len(velArr) > 1 else 0
        # helper.DeviationWindowDistances = st.stdev(distArr) if len(distArr) > 1 else 0
        print(dict(helper))
        i += 1
        helperArr.append(helper)
    return helperArr

def calculateML(pointList):
    start = time.process_time()
    XArr = np.empty([1,3])
    YArr = np.empty([1])
    XArr2 = np.empty([1,3])
    YArr2 = np.empty([1])
    for i, point in enumerate(pointList):
        tmpArr = list()
        for item in point:
            el = dict(item)
            tmpArr.append(el)
        values = pd.DataFrame(tmpArr, columns=['Data', 'VEL', 'DBP', 'FIX'])
        array = values.values
        X = array[:,0:3]
        Y = array[:,3]
        Y=Y.astype('int')
        if len(X) != len(Y):
            print('W punkcie ' + i + ' jest bład')
        if i < 3:
            XArr = np.concatenate([XArr,X])
            YArr = np.concatenate([YArr,Y])
        else:
            XArr2 = np.concatenate([XArr2,X])
            YArr2 = np.concatenate([YArr2,Y])
    print(XArr[1:,1:])
    model = LogisticRegression()
    model.fit(XArr[1:,1:], YArr[1:])

    prediction = model.predict(XArr2[1:,1:])
    
    ite = accuracy_score(YArr2[1:], prediction)
    print(ite)
    endXArr = np.concatenate([XArr[1:,:],XArr2[1:,:]])
    endYArr = np.concatenate([YArr[1:],prediction])
    endAll = np.c_[endXArr,endYArr]

    retX = []
    retY = []
    print(endAll)
    for item in endAll:
        if item[3] == 1:
            retX.append(item[0].CoordX)
            retY.append(item[0].CoordY)
    end = time.process_time()
    return retX, retY, len(retX), end - start, ite