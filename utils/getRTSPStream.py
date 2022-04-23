"""
+============================================================+
- Tác Giả: Hoàng Thành
- Viện Toán Ứng dụng và Tin học(SAMI - HUST)
- Email: thanh.hoangvan051199@gmail.com
- Github: https://github.com/thanhhoangvan
+============================================================+
# Test on ip camera Yossee

"""

import fractions
import os
import time
from threading import Thread
from multiprocessing import Process, Array, Value, Lock

import cv2

os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

def get_RTSP_URL(username, password, ip, port):
    return ('rtsp://{}:{}@{}:{}/onvif1'.format(username, password, ip, port),
            'rtsp://{}:{}@{}:{}/onvif2'.format(username, password, ip, port))

class RTSPStream:
    def __init__(self, ip="192.168.53.109", port=554,
                 username='admin', password='admin',
                 HD_Frame=None, SD_Frame=None):

        self.IP          = ip
        self.PORT        = port
        self.user        = username
        self.passwd      = password
        self.mp_HD_Frame = HD_Frame
        self.mp_SD_Frame = SD_Frame

        (self.RTSP_URL_HD, self.RTSP_URL_SD) = get_RTSP_URL(self.user, self.passwd, self.IP, self.PORT)


        self.HD_CaptureThread = None
        self.SD_CaptureThread = None
        self.processCapture = None
        self.mp_running = False

    def start(self):
        if not self.running:
            print("RTSP Process is running!")
        
        else:
            self.running = True
            self.processCapture = Process()

    def capture(self, URL, mp_frame, mp_running):
        cap = cv2.VideoCapture(URL)

        while mp_running.value:
            try:
                _, frame = cap.read()
            except:
                print('Error when capture frame from', URL)
            mp_frame.arquire()
            mp_frame[:] = frame

    def update(self, mp_running):
        if self.HD_CaptureThread is None:
            self.HD_CaptureThread = Thread(target=self.capture, args=(self.RTSP_URL_HD,
                                                                      self.mp_HD_Frame,
                                                                      self.mp_running))
        if self.SD_CaptureThread is None:
            self.SD_CaptureThread = Thread(target=self.capture, args=(self.RTSP_URL_HD,
                                                                      self.mp_SD_Frame,
                                                                      self.mp_running))
        self.HD_Capture.start()
        self.SD_Capture.start()

    def stop(self):
        pass

if __name__=='__main__':
    pass