import datetime
import os

class Data:
    def __init__(self, _type, timeStamp, coordX, coordY):
        self.Type = _type
        self.CoordX = coordX
        self.CoordY = coordY
        #self.TimeStamp = self.convertToReadableDate(int(timeStamp))
        self.TimeStamp = timeStamp

    def convertToReadableDate(self, timestamp):
        return datetime.datetime.fromtimestamp(timestamp / 1e3).strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]