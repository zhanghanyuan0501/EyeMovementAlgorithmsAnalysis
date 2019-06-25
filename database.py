import os, pymongo, json
from bson import json_util
import collections
import Data

def initialize_db(pointsList):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    myclient.drop_database("mydatabase")
    col = mydb["elements"]
    odbcarr = []
    i = 0
    #list = map(pointsList, )
    for element in list(pointsList):
        for value in element:
            doc = collections.OrderedDict()
            doc['id'] = i
            doc['Type'] = value.Type
            doc['CoordX'] = value.CoordX
            doc['CoordY'] = value.CoordY
            doc['TimeStamp'] = value.TimeStamp
            odbcarr.append(doc)
            i += 1
    #jsonArr = json.dumps(odbcarr, default=json_util.default)
    #print(jsonArr)
    col.insert_many(odbcarr)
    print(col)