import cv2 as cv 
import mediapipe as mp 
import time 


"""                static_image_mode=False,
               model_complexity=1,
               smooth_landmarks=True,
               enable_segmentation=False,
               smooth_segmentation=True,
               min_detection_confidence=0.5,
               min_tracking_confidence=0.5
 """


class PoseDetector():

    def __init__(self , mode = False , complexcity = 1 , smooth = True , detectionCov = .5 , trackingCof = .5,
                  enable = False , segment = True ) -> None:
        
        self.mode = mode 
        self.complexity = complexcity
        self.smooth = smooth
        self.detectionCov =detectionCov
        self.trackingCov = trackingCof
        self.enable = enable 
        self.segment = segment
        self.mpPose = mp.solutions.pose 
        self.pose = self.mpPose.Pose(self.mode, self.complexity , self.smooth , self.enable , self.segment,self.detectionCov , self.trackingCov)
        self.mpDraw = mp.solutions.drawing_utils
    
    def findpose(self , img , draw = True):
        imgRGB = cv.cvtColor(img , cv.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:  
                self.mpDraw.draw_landmarks(img , self.results.pose_landmarks , self.mpPose.POSE_CONNECTIONS)

        return img 
    
    def findposition(self , img , draw = True ):
        lmlist = []
        if self.results.pose_landmarks :
            for id , lm in enumerate(self.results.pose_landmarks.landmark):
                h , w, c = img.shape
                #print(id , lm )
                cx , cy = int(lm.x*w) , int(lm.y*h)
                lmlist.append([id , cx , cy])
                if draw:
                    cv.circle(img , (cx,cy), 5 , (0,0,255) , cv.FILLED)
        return lmlist
    
def main():
    cap = cv.VideoCapture(0)
    cTime = 0
    pTime = 0
    detector = PoseDetector()

    while True :

        succes , img = cap.read()
        img = detector.findpose(img)
        lmlist = detector.findposition(img)
        print(lmlist)
        cTime =time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime 

        cv.putText(img , str(int(fps)) ,(70,50), cv.FONT_HERSHEY_PLAIN , 3 , (255,0,255) , 3 )

        cv.imshow("Image" , img)

        if cv.waitKey(20) & 0xFF==ord('d'):##means if key d is pressed break out of the video
            break

if __name__ == "__main__" :
    main()