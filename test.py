import os
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
import time

import cv2
import numpy as np
from multiprocessing import Process, Array, Lock

RTSP_URL1 = 'rtsp://admin:hoangthanh1999@192.168.53.109:554/onvif1'
RTSP_URL2 = 'rtsp://admin:hoangthanh1999@192.168.53.109:554/onvif2'
 
time_start = time.time()
cap1 = cv2.VideoCapture(RTSP_URL1, cv2.CAP_FFMPEG)
cap2 = cv2.VideoCapture(RTSP_URL2, cv2.CAP_FFMPEG)
time_stop = time.time()
print('start after {} seconds'.format(time_stop - time_start))
font = cv2.FONT_HERSHEY_SIMPLEX

if not cap2.isOpened() or not cap1.isOpened():
   print('Cannot open RTSP stream')
   exit(-1)

mp_frame = Array("I", int(np.prod((360, 640, 3))), lock=Lock())
np_frame = np.frombuffer(mp_frame.get_obj(), dtype="I").reshape((360,640,3))

while True:
    time_0 = time.time()
    _, frame1 = cap1.read()
    time_1 = time.time()
    _, frame2 = cap2.read()
    time_2 = time.time()

    fps1 = int(1/(time_1-time_0))
    fps2 = int(1/(time_2-time_1))
    cv2.putText(frame1, str(fps1), (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)
    cv2.putText(frame2, str(fps2), (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

    # print(frame2.shape)
    mp_frame[:] = frame2.flatten()

    print('time:', time.time()  - time_2)
    # print("FPS: FullHD - {} | SD - {}".format(fps1, fps2))
    # print(frame1.shape, frame2.shape)

    img = np_frame.astype("uint8").copy()
    cv2.imshow('RTSP stream', img)
 
    if cv2.waitKey(1) == 27:
        break

cap2.release() 
cap2.release()
cv2.destroyAllWindows()