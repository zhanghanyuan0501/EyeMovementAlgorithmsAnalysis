import datetime
import os

class Data:
    def __init__(self, _type, timeStamp, coordX, coordY):
        self.Type = _type
        self.CoordX = float(coordX)
        self.CoordY = float(coordY)
        #self.TimeStamp = self.convertToReadableDate(int(timeStamp))
        self.TimeStamp = timeStamp