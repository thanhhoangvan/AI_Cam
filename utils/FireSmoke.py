"""
+============================================================+
- Tác Giả: Hoàng Thành
- Viện Toán Ứng dụng và Tin học(SAMI - HUST)
- Email: thanh.hoangvan051199@gmail.com
- Github: https://github.com/thanhhoangvan
+============================================================+
"""

import os
import time
from multiprocessing import Process, Array, Lock

import cv2

class FireDetection:
    def __init__(self):
        self.fire_cascade = cv2.CascadeClassifier('../models/fire_detection.xml')

    def detect(self, image):
        return self.fire_cascade.detectMultiScale(image, 1.2, 5)

    def show(self, image):
        fire = self.detect(image)
        for (x, y, w, h) in fire:
            cv2.rectangle(image,(x-20,y-20),(x+w+20,y+h+20),(255,0,0),2)
        return image


if __name__=='__main__':
    cam = cv2.VideoCapture(0)
    Fire = FireDetection()
    while True:
        ret, frame = cam.read()
        if ret:
            image = Fire.show(frame)
            
            cv2.imshow("Fire detection", image)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break