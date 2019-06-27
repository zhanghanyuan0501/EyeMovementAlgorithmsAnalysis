import os, pymongo, json
from bson import json_util
import collections
from Data import Data
import time

def initialize_db(pointsList):
        start = time.process_time()
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydatabase"]
        myclient.drop_database("mydatabase")
        col = mydb["elements"]
        odbcarr = []
        for element in list(pointsList):
                for value in element:
                        doc = collections.OrderedDict()
                        doc['Type'] = value.Type
                        doc['CoordX'] = value.CoordX
                        doc['CoordY'] = value.CoordY
                        doc['TimeStamp'] = value.TimeStamp
                        odbcarr.append(doc)
        col.insert_many(odbcarr)
        end = time.process_time()
        return '%.3f' % (end - start)

def getFromDatabase():
        start = time.process_time()
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["mydatabase"]
        elements = mydb["elements"].find()
        dataArray = []
        for element in elements:
                item = Data(element['Type'], element['TimeStamp'], element['CoordX'], element['CoordY'])
                dataArray.append(item)
        i = 0
        loopFlag = True
        retList = []
        returnList = []
        while loopFlag:
                for element in dataArray:
                        if i + 1 == len(dataArray):
                                retList.append(dataArray[i])
                                loopFlag = False
                                break
                        if dataArray[i + 1].Type == 'SS':
                                retList.append(dataArray[i])
                                break
                        retList.append(dataArray[i])
                        i += 1
                i += 1
                returnList.append(retList)
                retList = []

        end = time.process_time()
        return returnList, '%.3f' % (end - start)