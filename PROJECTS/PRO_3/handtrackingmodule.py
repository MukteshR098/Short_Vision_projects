import cv2 as cv 
import mediapipe as mp
import time

class handDetector():
    def __init__(self ,mode = False , maxhands = 4, detectionCon = 0.5 , trackingCon = 0.5 ) -> None:

        self.mode= mode 
        self.maxhands = maxhands
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxhands,
                                         min_detection_confidence=self.detectionCon, min_tracking_confidence=self.trackingCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipids = [ 4,8,12,16,20]

    def findhands(self , img , draw = True):
        imgRGB = cv.cvtColor(img , cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)
            
        if self.results.multi_hand_landmarks :
            for handlms in self.results.multi_hand_landmarks:
                if draw :
                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img 
    
    def findpostion(self , img , handNumber = 0 , draw = True):
        self.lmlist = []
        if self.results.multi_hand_landmarks :
            myhand = self.results.multi_hand_landmarks[handNumber]
            for id, lm in enumerate(myhand.landmark):
                        #print(id, lm) 
                        #Converting into pixels 
                h , w , c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                        #print(id , cx, cy)
                self.lmlist.append([id, cx, cy])
                if draw:
                    cv.circle(img,(cx,cy) ,5,(255,0,255),cv.FILLED)
        return self.lmlist

    def fingersup(self):
        fingers = []

        #THUMB
        if self.lmlist[4][1] < self.lmlist[self.tipids[0] - 1][1] :
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):#for fingers no thumb
            if self.lmlist[self.tipids[id]][2] < self.lmlist[self.tipids[id] - 2][2]:#Open cv ke hisab se likha hai 50>100 in open cv top se start hota hai
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers


def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture(0)
    
    detector = handDetector()

    while True:
        successs , img = cap.read()
        img = detector.findhands(img)
        lmlist = detector.findpostion(img)
        if len(lmlist) != 0:
            print(lmlist[4])

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv.putText(img , str(int(fps)), (10,70), cv.FONT_HERSHEY_PLAIN , 3 , (255,0,255), 3)

        cv.imshow("Image" , img)

        if cv.waitKey(20) & 0xFF==ord('d'):##means if key d is pressed break out of the video
            break

if __name__== "__main__" :
     print("jai shree ram")
     main()