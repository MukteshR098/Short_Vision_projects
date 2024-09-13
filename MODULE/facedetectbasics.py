import cv2 as cv 
import mediapipe as mp 
import time 

mpFace =mp.solutions.face_detection
mpDraw = mp.solutions.drawing_utils
faceDetect = mpFace.FaceDetection()

cap =  cv.VideoCapture(0)
cTime = 0
pTime =  0

while True :
    success , img = cap.read()
    imgRGB = cv.cvtColor(img , cv.COLOR_BGR2RGB)
    results = faceDetect.process(imgRGB)
    #print(results)#give class 

    if results.detections:
        for id , detection in enumerate(results.detections):
            #mpDraw.draw_detection(img , detection)
            h , w, c =  img.shape
            # print(detection)
            # print(detection.score) 
            # print(detection.location_data.relative_bounding_box.xmin)
            bboxC = detection.location_data.relative_bounding_box
            bbox = int(bboxC.xmin * w) , int(bboxC.ymin * h) , int(bboxC.width*w) , int(bboxC.height*h)

            cv.rectangle(img ,bbox , (0,255,0) , 2 )
            cv.putText(img , f'{int(detection.score[0]*100)}%' , (bbox[0], bbox[1] - 20), cv.FONT_HERSHEY_SCRIPT_COMPLEX , 3, (0,255,0), 2)

    cTime = time.time()
    fps = 1/ (cTime - pTime)
    pTime = cTime 

    cv.putText(img , str(int(fps)), (50,70) , cv.FONT_HERSHEY_COMPLEX , 3 , (0,255,255), 3)
    cv.imshow("Image" , img )

    if cv.waitKey(20) & 0xFF==ord('d'):
        break 

