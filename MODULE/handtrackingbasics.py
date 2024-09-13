import cv2 as cv 
import mediapipe as mp
import time

##WEB cam ke liye hai ye 
cap = cv.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    successs , img = cap.read()
    imgRGB = cv.cvtColor(img , cv.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks :
        for handlms in results.multi_hand_landmarks:
            for id, lm in enumerate(handlms.landmark):
               #print(id, lm) 

               ##Converting into pixels 
               h , w , c = img.shape
               cx,cy = int(lm.x*w), int(lm.y*h)
               #print(id , cx, cy)
               if id==4:
                   cv.circle(img,(cx,cy) , 25,(255,0,255),cv.FILLED)


            mpDraw.draw_landmarks(img, handlms, mpHands.HAND_CONNECTIONS)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv.putText(img , str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN , 3 , (255,0,255), 3)

    cv.imshow("Image" , img)

    if cv.waitKey(20) & 0xFF==ord('d'):##means if key d is pressed break out of the video
        break



"""   def rescaleFrame(frame , scale=0.75):
    width = int(frame.shape[1]*0.75)
    height = int(frame.shape[0]*0.75)

    dimension = (width,height)
    return cv.resize(frame, dimension , interpolation = cv.INTER_AREA)

#Reading Videos 
capture = cv.VideoCapture("Resources/Videos/dog.mp4")

##Resolution Change 
def changeRes(width,height):
    ##only work for Live video 
    capture.set(3,width)
    capture.set(4,height)


while True:
    isTrue , frame = capture.read()

    frame_resized = rescaleFrame(frame)
    cv.imshow('Video', frame)
    cv.imshow('Video Resized', frame_resized)

    if cv.waitKey(20) & 0xFF==ord('d'):##means if key d is pressed break out of the video
        break

capture.release()
cv.destroyAllWindows() """