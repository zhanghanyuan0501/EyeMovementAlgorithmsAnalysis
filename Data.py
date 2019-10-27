import datetime
import os

class Data:
    def __init__(self, _type, timeStamp, coordX, coordY):
        self.Type = _type
        self.CoordX = float(coordX)
        self.CoordY = float(coordY)
        self.TimeStamp = timeStamp

    def __iter__(self):
        yield 'Type', self.Type
        yield 'CoordX', self.CoordX
        yield 'CoordY', self.CoordY
        yield 'TimeStamp', self.TimeStamp