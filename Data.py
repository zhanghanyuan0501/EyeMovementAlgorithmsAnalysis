import datetime
import os

class Data:
    def __init__(self, _type, timeStamp, coordX, coordY):
        self.Type = _type
        self.CoordX = coordX
        self.CoordY = coordY
        self.TimeStamp = timeStamp