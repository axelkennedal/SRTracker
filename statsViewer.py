import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

plt.rcParams['toolbar'] = 'None'
import matplotlib.ticker as plticker
import numpy as np
import os
from tinydb import TinyDB, Query
dbLocation = os.getcwd() + "/SRdb.json"
print("loading data from", dbLocation)
db = TinyDB(dbLocation)

def addLabels(tankSR, damageSR, supportSR):
    yValues = (tankSR, damageSR, supportSR)
    for listOfYValues in yValues:
        # zip joins x and y coordinates in pairs
        for x,y in zip(xValues, listOfYValues):
            plt.annotate(y, # this is the text
                        (x,y), # this is the point to label
                        textcoords="offset points", # how to position the text
                        xytext=(0,10), # distance from text to points (x,y)
                        fontsize=4,
                        ha='center') # horizontal alignment can be left, right or center

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
maxSR = 3200
yTickFrequency = (maxSR - minSR) / 10

axes = plt.gca()
axes.set_ylim([minSR, maxSR])

plt.yticks(np.arange(minSR, maxSR, yTickFrequency))
print("tankSR:", tankSR)
print("damageSR:", damageSR)
print("supportSR:", supportSR)

plt.title("Overwatch SR Over Time, " + str(len(allStats)) + " games")
plt.plot(xValues, tankSR, label="Tank SR")
plt.plot(xValues, damageSR, label="Damage SR")
plt.plot(xValues, supportSR, label="Support SR")
plt.legend(loc="upper left")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.02),
          fancybox=True, shadow=True, ncol=5)
plt.xticks([])


plt.show()