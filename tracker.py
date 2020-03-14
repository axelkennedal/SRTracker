# cv2.cvtColor takes a numpy ndarray as an argument 
import numpy as nm 
  
import pytesseract 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

# importing OpenCV 
import cv2
from PIL import ImageGrab, Image, ImageEnhance
  
import datetime
import time

import os

from tinydb import TinyDB, Query
dbLocation = os.getcwd() + "/SRdb.json"
print("saving data to", dbLocation)
db = TinyDB(dbLocation)

# general dimensions
SRTextWidth = 62
SRTextHeight = 40
topOffset = 555

def getSR(img, leftOffsetPx):
    cropSize = (leftOffsetPx, topOffset, leftOffsetPx+SRTextWidth, topOffset+SRTextHeight)
    cropped = img.crop(cropSize)
    processed = ImageEnhance.Contrast(cropped).enhance(2)
    return makeInt(pytesseract.image_to_string(cv2.cvtColor(nm.array(processed), cv2.COLOR_BGR2GRAY), lang="eng"))

def makeInt(someString):
    try:
        return int(someString.strip())
    except:
        return -1

def difference(numA, numB):
    if (numA == -1 or numB == -1):
        return 0
    else:
        return abs(numA - numB)

# max change allowed in SR between two games, used to reduce number of incorrect readings
SR_DIFF_TOLERANCE = 60
SR_MIN = 500
SR_MAX = 4800
def shouldSaveStats(tankSR, damageSR, supportSR):
    if (tankSR == -1 and damageSR == -1 and supportSR == -1):
        return False

    allEntries = db.all()
    if (len(allEntries) > 0):
        lastEntry = allEntries[-1]

        if (tankSR == lastEntry["tankSR"] and damageSR == lastEntry["damageSR"] and supportSR == lastEntry["supportSR"]):
            return False

    return True

img = Image.open(os.getcwd() + "\SRimage_hover.png")
tankLeftOffset = 860 # not right
damageLeftOffset = 940
supportLeftOffset = 1220

starttime=time.time()
secondsBetweenUpdate = 5
while True:
    print("Analyzing screen...")
    img = ImageGrab.grab()
    tankSR = getSR(img, tankLeftOffset)
    damageSR = getSR(img, damageLeftOffset)
    supportSR = getSR(img, supportLeftOffset)
    captureTime = datetime.datetime.now()

    if (shouldSaveStats(tankSR, damageSR, supportSR)):
        allEntries = db.all()
        if (len(allEntries) > 0):
            lastEntry = allEntries[-1]
            if ((difference(tankSR, lastEntry["tankSR"]) > SR_DIFF_TOLERANCE)):
                tankSR = lastEntry["tankSR"]
            if (difference(damageSR, lastEntry["damageSR"]) > SR_DIFF_TOLERANCE):
                damageSR = lastEntry["damageSR"]
            if (difference(supportSR, lastEntry["supportSR"]) > SR_DIFF_TOLERANCE):
                supportSR = lastEntry["supportSR"]
        
        if (not shouldSaveStats): continue

        print("saving stats")
        print("time:", str(captureTime))
        print("Tank SR:", tankSR)
        print("Damage SR:", damageSR)
        print("Support SR:", supportSR)
        db.insert({"captureTime" : str(captureTime), "tankSR" : tankSR, "damageSR" : damageSR, "supportSR" : supportSR})
    else:
        print("not saving stats")
    time.sleep(secondsBetweenUpdate - ((time.time() - starttime) % secondsBetweenUpdate))