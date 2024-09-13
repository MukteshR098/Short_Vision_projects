import cv2 as cv 
import mediapipe as mp 
import os 
import time 
import handtrackingmodule as htm 

wCam , hCam = 1280, 720

cTime = 0
pTime = 0

cap = cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

detector = htm.handDetector(detectionCon=.85)


while True:
    success , img = cap.read()
    img = cv.flip(img, 1)

    #Find Landmarks 
    img = detector.findhands(img)
    lmlist = detector.findpostion(img, draw=False)
    

    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1] , lmlist[8][2]
        x2 , y2 = lmlist[12][1:]

        fingers = detector.fingersup()

        if fingers[1] and fingers[2]:
            cv.rectangle(img , (x1,y1-25) , (x2, y2+25), (255,0,255), cv.FILLED)
            print("selction mode")
            #Checking for the click 
            if y1 < 125:
                if 250<x1<450:
                    

        if fingers[1] and fingers[2]==False:
            cv.circle(img ,(x1, y1) , 15  , (255,0,255),cv.FILLED)
            print("Drawing Mode")





    cv.imshow("Image" , img )
    if cv.waitKey(20) & 0xFF==ord('d'):
        break 