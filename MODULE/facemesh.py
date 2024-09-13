import cv2 as cv 
import mediapipe as mp
import time 

mpFaceMesh = mp.solutions.face_mesh
mesh = mpFaceMesh.FaceMesh(max_num_faces =2)
mpDraw= mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles


cap = cv.VideoCapture(0)
cTime = 0 
pTime = 0
while True:

    success , img = cap.read()
    imgRGB = cv.cvtColor(img , cv.COLOR_BGR2RGB)
    results = mesh.process(imgRGB)
    if results.multi_face_landmarks : 
        for facelms in results.multi_face_landmarks:
            mpDraw.draw_landmarks(img , facelms ,mpFaceMesh.FACEMESH_TESSELATION ,None , mp_drawing_styles
            .get_default_face_mesh_tesselation_style() )

            for id , lm in enumerate(facelms.landmark):
                #print(id , lm)
                h , w , c = img.shape
                x , y =int(lm.x*w) , int(lm.y*h)
                print(x , y)



    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime 

    cv.putText(img , f" FPS: {int(fps)}", (20,50) , cv.FONT_HERSHEY_PLAIN , 2 , (255,0,25), 2)

    cv.imshow("Image" , img )

    if cv.waitKey(20) & 0xFF==ord('d'):
        break 