import datetime
import matplotlib.pyplot as plt

def convertToReadableDate(timestamp):
    return datetime.datetime.fromtimestamp(timestamp / 1e3).strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]

def plotResults(coordX, coordY, title):
    plt.plot(coordX, coordY, 'ro')
    plt.title(title + ' Number of fixations' + str(len(coordX)))
    plt.show()