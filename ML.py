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
        self.id = int(0)
        self.Data = Data(Type, TimeStamp, CoordX, CoordY)
        self.VelocityBetweenPoints = float(0)
        self.DistancesBetweenPoints = float(0)
        self.DistancesWindow = float(0)
        self.AverageVelocityInWindow = float(0)
        self.DeviationWindowVelocity = float(0)
        self.DeviationWindowDistances = float(0)
        self.IsFixation = bool

    def __iter__(self):
        yield 'id', self.id
        yield 'Vel', self.VelocityBetweenPoints
        yield 'IsFixation', 1 if self.IsFixation == True else 0



def calculateMlHelper(pointList, existingFixations):
    i = 0
    j = 0
    helperArr = []
    while i < len(pointList):
        helper = MLHelper(pointList[i].Type, pointList[i].CoordX, pointList[i].CoordY, pointList[i].TimeStamp)
        helper.id = i+1
        helper.IsFixation = pointList[i] in existingFixations
        if helper.IsFixation is True:
            j+=1
        if i+1 < len(pointList):
            helper.VelocityBetweenPoints = ivt.calculateVelocitiesBetweenPoints(pointList[i], pointList[i + 1])
        i += 1
        helperArr.append(helper)
    return helperArr


def calculateML(pointList):
    XArr = np.empty([1,2])
    YArr = np.empty([1])
    XArr2 = np.empty([1,2])
    YArr2 = np.empty([1])
    for i, point in enumerate(pointList):
        tmpArr = list()
        for item in point:
            el = dict(item)
            tmpArr.append(el)
        values = pd.DataFrame(tmpArr)
        array = values.values
        X = array[:,0:2]
        Y = array[:,2]
        
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
    
    ite = np.sum(YArr2[1:] == prediction)
    print(ite)
    print(prediction)
    retX = np.concatenate([XArr[1:,1:],XArr2[1:,1:]])
    
