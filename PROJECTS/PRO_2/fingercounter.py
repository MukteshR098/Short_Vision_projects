import cv2 as cv 
import mediapipe 
import time 
import os 
import handtrackingmodule as htm 


wCam  , hCam = 640, 480

cap = cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4 , hCam)

cTime = 0
pTime = 0

detector =htm.handDetector(detectionCon= .75)

tipids = [4,8,12,16,20]

while True:

    success , img = cap.read()

    img = detector.findhands(img )
    lmlist = detector.findpostion(img , draw=False)
    #print(lmlist)
    if len(lmlist) != 0:
        fingers = []

        #THUMB
        if lmlist[4][1] > lmlist[tipids[0] - 1][1] :
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):#for fingers no thumb
            if lmlist[tipids[id]][2] < lmlist[tipids[id] - 2][2]:#Open cv ke hisab se likha hai 50>100 in open cv top se start hota hai
                fingers.append(1)
            else:
                fingers.append(0)
        #print(fingers)
        totalFingers = fingers.count(1)
        print(totalFingers)

        cv.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv.FILLED)
        cv.putText(img, str(totalFingers), (45, 375), cv.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)



    cTime =time.time()
    fps = 1/(cTime -pTime)
    pTime = cTime
    cv.putText(img , f"FPS : {int(fps)}", (20,50), cv.FONT_HERSHEY_SCRIPT_COMPLEX , 2 , (20,10,30) , 2)


    cv.imshow("Image" , img)

    if cv.waitKey(20) & 0xFF==ord("d") :
        break 

