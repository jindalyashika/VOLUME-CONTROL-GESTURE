import cv2
import time
import numpy as np
import hand_tracking_module as htm
import math
from ctypes import cast,POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

######################
wCam,hCam = 480,720                   # to make web cam size bigger
######################
#  to run the pyhon file
volRange=volume.GetVolumeRange()
minVol= volRange[0]
maxVol= volRange[1]
vol=0
volBar=400
volPer=0
frame_skip = 4  # Skip every second frame
frame_counter = 0


while True:
    frame_counter += 1
    sucess,img=cap.read()
    if frame_counter % frame_skip == 0:  # Only process every second frame
        
     img=detector.findHands(img)
     lmList= detector.findPosition(img,draw=False)
     if len(lmList) !=0:
        # print(lmList[4],lmList[8])
        
        x1,y1= lmList[4][1],lmList[4][2]
        x2,y2= lmList[8][1],lmList[8][2]
        cx,cy=(x1+x2)//2 ,(y1+y2)//2
        
        cv2.circle(img,(x1,y1),10,(230,0,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),10,(230,0,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(230,0,0),2)
        cv2.circle(img,(cx,cy),5,(0,0,220),cv2.FILLED)
        
        
        length= math.hypot(x2-x1, y2-y1)                       #to print the length of the line         
        # print(length)
        
        #Hand range 50-200
        #volRange = -65 -0
        
        vol= np.interp(length,[60,200],[minVol,maxVol])
        volBar= np.interp(length,[60,200],[400,150])
        volPer= np.interp(length,[60,200],[0,100])

        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length<60:
            cv2.circle(img,(cx,cy),5,(0,220,0),cv2.FILLED)

    cv2.rectangle(img,(60,150),(85,400),(140,0,0),3)                       # create rec v1(initial pos) v2(ending pos)
    cv2.rectangle(img,(60,int(volBar)),(85,400),(140,0,0),cv2.FILLED)
    cv2.putText(img,f'{int(volPer)}%',(60,450),cv2.FONT_HERSHEY_COMPLEX,1,(140,0,0),3)


    
    cTime= time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img,f'FPS:{str(int(fps))}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(140,0,0),3,)

    cv2.imshow("Img",img)
    key=cv2.waitKey(1)
    if key == ord('q'):
        break