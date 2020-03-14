# cv2.cvtColor takes a numpy ndarray as an argument 
import numpy as nm 
  
import pytesseract 
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

# importing OpenCV 
import cv2
from PIL import ImageGrab, Image
  
import datetime
import time

# general dimensions
SRTextWidth = 60
SRTextHeight = 40
topOffset = 555

def getSR(img, leftOffsetPx):
    cropSize = (leftOffsetPx, topOffset, leftOffsetPx+SRTextWidth, topOffset+SRTextHeight)
    cropped = img.crop(cropSize)
    return makeInt(pytesseract.image_to_string(cv2.cvtColor(nm.array(cropped), cv2.COLOR_BGR2GRAY), lang="eng"))

def makeInt(someString):
    someString = someString.strip()
    return int(someString) if someString else None

img = Image.open(r"C:\Users\darkm0de\Pictures\SRimage.png")
tankLeftOffset = 860 # not right
damageLeftOffset = 940
supportLeftOffset = 1220

starttime=time.time()
secondsBetweenUpdate = 5
while True:
    img = ImageGrab.grab()
    print("time:", str(datetime.datetime.now()))
    print("Tank SR:", getSR(img, tankLeftOffset))
    print("Damage SR:", getSR(img, damageLeftOffset))
    print("Support SR:", getSR(img, supportLeftOffset))
    time.sleep(secondsBetweenUpdate - ((time.time() - starttime) % secondsBetweenUpdate))