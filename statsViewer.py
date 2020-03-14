import matplotlib.pyplot as plt
plt.rcParams['toolbar'] = 'None'
import matplotlib.ticker as plticker
import numpy as np
import os
from tinydb import TinyDB, Query
dbLocation = os.getcwd() + "/SRdb.json"
print("loading data from", dbLocation)
db = TinyDB(dbLocation)

allStats = db.all()
print("allStats:", allStats)
tankSR = []
damageSR = []
supportSR = []
for entry in allStats:
    tankSR.append(entry["tankSR"])
    damageSR.append(entry["damageSR"])
    supportSR.append(entry["supportSR"])

xValues = range(0, len(allStats))

minSR = 2000
maxSR = 3500
yTickFrequency = (maxSR - minSR) / 10

axes = plt.gca()
axes.set_ylim([minSR, maxSR])
plt.yticks(np.arange(minSR, maxSR, yTickFrequency))
print("tankSR:", tankSR)
print("damageSR:", damageSR)
print("supportSR:", supportSR)

plt.title("Overwatch SR Over Time")
plt.plot(xValues, tankSR, label="Tank SR", marker='o')
plt.plot(xValues, damageSR, label="Damage SR", marker='o')
plt.plot(xValues, supportSR, label="Support SR", marker='o')
plt.legend(loc="upper left")
plt.xticks([])

yValues = (tankSR, damageSR, supportSR)
for listOfYValues in yValues:
    # zip joins x and y coordinates in pairs
    for x,y in zip(xValues, listOfYValues):
        plt.annotate(y, # this is the text
                    (x,y), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0,10), # distance from text to points (x,y)
                    fontsize=8,
                    ha='center') # horizontal alignment can be left, right or center

plt.show()