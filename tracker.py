# cv2.cvtColor takes a numpy ndarray as an argument 
import numpy as nm 
  
import pytesseract 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

# importing OpenCV 
import cv2
from PIL import ImageGrab, Image
  
import datetime
import time

import os

from tinydb import TinyDB, Query
dbLocation = os.getcwd() + "/SRdb.json"
print("saving data to", dbLocation)
db = TinyDB(dbLocation)

# general dimensions
SRTextWidth = 60
SRTextHeight = 40
topOffset = 555

def getSR(img, leftOffsetPx):
    cropSize = (leftOffsetPx, topOffset, leftOffsetPx+SRTextWidth, topOffset+SRTextHeight)
    cropped = img.crop(cropSize)
    return makeInt(pytesseract.image_to_string(cv2.cvtColor(nm.array(cropped), cv2.COLOR_BGR2GRAY), lang="eng"))

def makeInt(someString):
    try:
        return int(someString.strip())
    except:
        return -1

def shouldSaveStats(tankSR, damageSR, supportSR):
    if (tankSR == -1 and damageSR == -1 and supportSR == -1):
        return False

    lastEntry = db.all()[-1]
    if (tankSR == lastEntry["tankSR"] and damageSR == lastEntry["damageSR"] and supportSR == lastEntry["supportSR"]):
        return False
    
    return True

img = Image.open(os.getcwd() + "\SRimage.png")
tankLeftOffset = 860 # not right
damageLeftOffset = 940
supportLeftOffset = 1220

starttime=time.time()
secondsBetweenUpdate = 5
while True:
    img = ImageGrab.grab()
    tankSR = getSR(img, tankLeftOffset)
    damageSR = getSR(img, damageLeftOffset)
    supportSR = getSR(img, supportLeftOffset)
    captureTime = datetime.datetime.now()
    print("time:", str(captureTime))
    print("Tank SR:", tankSR)
    print("Damage SR:", damageSR)
    print("Support SR:", supportSR)
    if (shouldSaveStats(tankSR, damageSR, supportSR)):
        print("saving stats")
        db.insert({"captureTime" : str(captureTime), "tankSR" : tankSR, "damageSR" : damageSR, "supportSR" : supportSR})
    else:
        print("not saving stats")
    time.sleep(secondsBetweenUpdate - ((time.time() - starttime) % secondsBetweenUpdate))