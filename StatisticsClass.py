import os, time

class StatisticsClass:
    def __init__(self):
        self.ImportAndConvertFileStatistic = 0
        self.ImportDataToDatabase = 0
        self.ImportAndConvertDatabaseStatistic = 0
        self.CalibrationSummaryTime = float(0)
        self.AlgorithmRunTimeStatistic = 0
        self.NumberOfFixationsCount = 0
