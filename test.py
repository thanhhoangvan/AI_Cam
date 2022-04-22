import time
import cv2
import os
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

RTSP_URL1 = 'rtsp://admin:hoangthanh1999@192.168.53.109:554/onvif1'
RTSP_URL2 = 'rtsp://admin:hoangthanh1999@192.168.53.109:554/onvif2'
 
cap1 = cv2.VideoCapture(RTSP_URL1, cv2.CAP_FFMPEG)
cap2 = cv2.VideoCapture(RTSP_URL2, cv2.CAP_FFMPEG)

font = cv2.FONT_HERSHEY_SIMPLEX

if not cap2.isOpened() or not cap1.isOpened():
   print('Cannot open RTSP stream')
   exit(-1)
 
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

    print("FPS: FullHD - {} | SD - {}".format(fps1, fps2))

    cv2.imshow('RTSP stream', frame2)
 
    if cv2.waitKey(1) == 27:
        break

cap2.release() 
cap2.release()
cv2.destroyAllWindows()