import cv2 as cv 

import numpy as np 
import time
import handtrackingmodule as htm 
import math 
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam , hCam = 640, 480

cap = cv.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
cTime = 0
pTime = 0

detector = htm.handDetector(detectionCon=0.75)


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBAR = 400
volPer = 0

while True :
    success , img = cap.read()
    img = detector.findhands(img)
    lmlist = detector.findpostion(img , draw = False)
    if len(lmlist) != 0:
        #print(lmlist[4], lmlist[8])

        x1 , y1 = lmlist[4][1] , lmlist[4][2]
        x2, y2 = lmlist[8][1] , lmlist[8][2]
        cv.circle(img, (x1,y1) , 15 , (255 , 0, 255) , cv.FILLED)
        cv.circle(img, (x2,y2) , 15 , (255 , 0, 255) , cv.FILLED)
        cv.line(img , (x1 , y1), (x2,y2), (255 ,255 , 0), 3)

        cx, cy = (x1+x2)//2 , (y1+y2)//2
        cv.circle(img, (cx,cy) , 15 , (255 , 0, 255) , cv.FILLED)

        length = math.hypot(x2-x1 , y2-y1)
        #print(length)

        #handRange was 50(minimum) to 300(Maximum) 
        #Vol Range -65 to 0
        vol = np.interp(length , [50,200] , [minVol,maxVol])
        volBAR = np.interp(length , [50,200] , [400,150]) 
        volPer = np.interp(length ,[50,200], [0,100])       
        print(vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<50:
            cv.circle(img, (cx,cy) , 15 , (0, 255, 0) , cv.FILLED)

    cv.rectangle(img , (50,150), (85,400), (0,255,0), 3)
    cv.rectangle(img , (50,int(volBAR)), (85,400), (0,255,0), cv.FILLED)        
    cv.putText(img , f"PerCent: {int(volPer)}%" ,(40,450), cv.FONT_HERSHEY_COMPLEX_SMALL , 1 , (0,255,0),3)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv.putText(img ,f"FPS: {int(fps)}" , (20,50), cv.FONT_HERSHEY_DUPLEX , 1 , (25,15,100), 1)

    cv.imshow("Image " , img)

    if cv.waitKey(20) & 0xFF==ord("d") :
        break




