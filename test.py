import time
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;0"
import cv2

vcap = cv2.VideoCapture("rtsp://admin:hoangthanh1999@192.168.53.109:554/onvif1")

while(1):
    ret, frame = vcap.read()
    if ret:
      cv2.imshow('VIDEO', frame)
      cv2.waitKey(0)