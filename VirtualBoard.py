import cv2
import numpy as np
import time
import os
import HTmodule as htm


brushThickness = 15
eraserThickness = 100

folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for impath in myList:
    image = cv2.imread(f'{folderPath}/{impath}')
    overlayList.append(image)
print(len(overlayList))

header = overlayList[0]
drawColor = (255, 0, 255)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.handDetector(detectionCon=0.85)
xp, yp = 0,0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

while True:

    #1 import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    #2 find hand landmarks
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList)!=0:
        #print(lmList)

        #tip of index and middle fingers--
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        #3 check which finger is up
        fingers = detector.fingersUp()
        print(fingers)

        #4 if selection mode -- two finger are up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            print("Selection mode")
            #checking for the click--
            if y1 < 125:
                if 300<x1<370:
                    header = overlayList[0]
                    drawColor = (0, 0, 0)
                elif 450<x1<570:
                    header =overlayList[1]
                    drawColor = (0, 255, 0)
                elif 630<x1<750:
                    header = overlayList[2]
                    drawColor = (0, 0, 255)
                elif 780<x1<890:
                    header = overlayList[3]
                    drawColor = (255, 0, 0)
                elif 910<x1<970:
                    header = overlayList[3]
                    drawColor = (255, 255, 255)
                elif 1000<x1<1030:
                    header = overlayList[3]
                    drawColor = (128, 128, 128)
            cv2.rectangle(img, (x1, y1 - 35), (x2, y2 + 35), drawColor, cv2.FILLED)

        #5 if drawing mode -- index finger is up
        if fingers[1] and fingers[2] == False:
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            print("Drwawing mode")
            if xp==0 and yp==0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:
                cv2.line(img, (xp,yp), (x1,y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    img[0:130, 0:1280] = header
    img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", img)
    cv2.waitKey(1)