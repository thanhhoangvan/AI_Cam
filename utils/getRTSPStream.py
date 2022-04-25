"""
+============================================================+
- Tác Giả: Hoàng Thành
- Viện Toán Ứng dụng và Tin học(SAMI - HUST)
- Email: thanh.hoangvan051199@gmail.com
- Github: https://github.com/thanhhoangvan
+============================================================+
# Test on ip camera Yossee

"""

import os
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

import json
import time
from threading import Thread
from multiprocessing import Process, Array, Value, Lock
from turtle import rt

import cv2
import numpy as np


def get_RTSP_URL(username, password, ip, port):
    return ('rtsp://{}:{}@{}:{}/onvif1'.format(username, password, ip, port), # Full HD rtsp url
            'rtsp://{}:{}@{}:{}/onvif2'.format(username, password, ip, port)) #      SD rtsp url

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
        self.mp_running = Value('I', 0)

    def start(self):
        if self.mp_running.value != 0:
            print("RTSP Process is running!")
        
        else:
            self.mp_running.value = 1
            self.processCapture = Process(target=self.update)
            self.processCapture.start()

    def capture(self, URL, mp_frame, mp_running):
        print("Start capture from", URL)
        cap = cv2.VideoCapture(URL)

        while mp_running.value == 1:
            ret, frame = cap.read()
            if ret:
                mp_frame.acquire()
                mp_frame[:] = frame.flatten()
                # try:
                #     # mp_frame.release()
                #     print('captured a frame from', URL)
                # except ValueError:
                #     print('Error when assign frame', URL)
            else:
                print('Can not capture from', URL)

            time.sleep(0.001)
        
        print("Stop capture from", URL)

    def update(self):
        if self.HD_CaptureThread is None:
            self.HD_CaptureThread = Thread(target=self.capture, args=(self.RTSP_URL_HD,
                                                                      self.mp_HD_Frame,
                                                                      self.mp_running))
        if self.SD_CaptureThread is None:
            self.SD_CaptureThread = Thread(target=self.capture, args=(self.RTSP_URL_SD,
                                                                      self.mp_SD_Frame,
                                                                      self.mp_running))
        self.HD_CaptureThread.start()
        self.SD_CaptureThread.start()
        
        while self.mp_running.value == 1:
            pass
            
        self.HD_CaptureThread.join()
        self.SD_CaptureThread.join()

    def stop(self):
        if self.mp_running.value == 1:
            self.mp_running.value = 0
        time.sleep(0.5)
        self.processCapture.join()

if __name__=='__main__':
    HD_RESOLUTION = (1080, 1920, 3)
    SD_RESOLUTION = (360, 640, 3)

    mp_FRAME_HD = Array("I", int(np.prod(HD_RESOLUTION)), lock=Lock())
    mp_FRAME_SD = Array("I", int(np.prod(SD_RESOLUTION)), lock=Lock())

    hd_nparray = np.frombuffer(mp_FRAME_HD.get_obj(), dtype="I").reshape(HD_RESOLUTION)
    sd_nparray = np.frombuffer(mp_FRAME_SD.get_obj(), dtype="I").reshape(SD_RESOLUTION)

    json_config = {}
    with open('./config.json', 'r') as json_file:
        json_config = json.load(json_file)

    IP = json_config['rtsp']['ip']
    PORT = json_config['rtsp']['port']
    USERNAME = json_config['rtsp']['username']
    PASSWORD = json_config['rtsp']['password']

    rtsp_stream = RTSPStream(ip=IP, port=PORT,
                             username=USERNAME, password=PASSWORD,
                             HD_Frame=mp_FRAME_HD, SD_Frame=mp_FRAME_SD)
    rtsp_stream.start()
    print('Start Successful!')
    
    start_time = time.time()
    while (time.time() - start_time) <= 30:
        hd_frame = sd_nparray.astype("uint8").copy()
        sd_frame = sd_nparray.astype("uint8").copy()
        
        cv2.imshow('RTSP Streamming Result', hd_frame)
        # cv2.imshow('RTSP Streamming Result', sd_frame)
        
        try:
            mp_FRAME_HD.release()
            mp_FRAME_SD.release()
        except ValueError:
            pass

            if cv2.waitKey(1) == 27:
                break
        time.sleep(0.001)
    
    cv2.destroyAllWindows()
    rtsp_stream.stop()    
    print('Stop Successful!')