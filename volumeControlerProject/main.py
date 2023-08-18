from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import cv2
import HandTrackingModule as htm
import time
import math
import numpy as np
from pyautogui import press,PAUSE

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


# volume.GetMute()
volume.GetMasterVolumeLevel()
volRange=(volume.GetVolumeRange())
maxVol=volRange[1]
minVol=volRange[0]
volume.SetMasterVolumeLevel(-20.0, None)
vol = 0
volBar = 400
volPer = 0
pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
wCam, hCam = 1240, 720
cap.set(3,wCam)
cap.set(4,hCam)
detector = htm.handDetector()
while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=True )
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
                # print(lmList[4],lmList[8])


                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]

                px1,py1= lmList[16][1],lmList[16][2]
                px2,py2= lmList[0][1],lmList[0][2]

                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2 #midpoint between index and thumb
                muteX ,muteY =(px1+px2)//2, (py1+py2)//2 #distance between ring and wrist

                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)#thumb
                cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)#index
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)#midpoint

                length = math.hypot(x2 - x1, y2 - y1)
                dist_R_W=math.hypot((px1-px2),(py1-py2))
                print(dist_R_W)

                vol = np.interp(length, [50, 300], [minVol, maxVol])
                volBar = np.interp(length, [50, 300], [400, 150])
                volPer = np.interp(length, [50, 300], [0, 100])
                # print(int(length), vol)
                volume.SetMasterVolumeLevel(vol, None)
                # if dist_R_W<250:
                #       if not PAUSE:
                #         press('space')  # Press the spacebar to play/pause the video
                #         PAUSE = True
                #       else:
                #         PAUSE = False

                # if dist_R_W < 250:
                #     press('space')

                if length < 50:
                    cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)


    cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,1, (255, 0, 0), 3)

    cTime = time.time()
    # print(cTime)
    fps = 1 / (cTime - pTime)
    # fps=int(cap.get(cv2.CAP_PROP_FPS))
    pTime = cTime


    cv2.putText(img, "FPS "+str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
               (255, 0, 255), 3)

    cv2.imshow("Image12", img)
    cv2.waitKey(1)