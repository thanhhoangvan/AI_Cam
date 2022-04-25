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
from multiprocessing import Process, Queue, Value, Lock

import cv2
import numpy as np


def get_RTSP_URL(username, password, ip, port):
    return ('rtsp://{}:{}@{}:{}/onvif1'.format(username, password, ip, port), # Full HD rtsp url
            'rtsp://{}:{}@{}:{}/onvif2'.format(username, password, ip, port)) #      SD rtsp url


class RTSPStream:
    def __init__(self, ip="192.168.53.109", port=554,
                 username='admin', password='admin',
                 queue_hd=None, queue_sd=None):

        self.IP          = ip
        self.PORT        = port
        self.user        = username
        self.passwd      = password
        self.queue_hd_frame = queue_hd
        self.queue_sd_frame = queue_sd

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
                if not mp_frame.full():
                    mp_frame.put(frame)
            else:
                print('Can not capture from', URL)

        print("Stop capture from", URL)

    def update(self):
        if self.HD_CaptureThread is None:
            self.HD_CaptureThread = Thread(target=self.capture, args=(self.RTSP_URL_HD,
                                                                      self.queue_hd_frame,
                                                                      self.mp_running))
        if self.SD_CaptureThread is None:
            self.SD_CaptureThread = Thread(target=self.capture, args=(self.RTSP_URL_SD,
                                                                      self.queue_sd_frame,
                                                                      self.mp_running))
        self.HD_CaptureThread.start()
        self.SD_CaptureThread.start()
        
        while True:
            if self.mp_running.value == 0:
                time.sleep(0.005)
                self.HD_CaptureThread.join()
                self.SD_CaptureThread.join()
                break
        print('Joined all threads')

    def stop(self):
        if self.mp_running.value == 1:
            self.mp_running.value = 0
        time.sleep(0.1)

        self.HD_CaptureThread = None
        self.SD_CaptureThread = None

        # Clean queue
        print('Cleanning queue....')
        while True:
            _ = self.queue_hd_frame.get()
            _ = self.queue_sd_frame.get()

            if  self.queue_hd_frame.empty():
                if  self.queue_sd_frame.empty():
                    break        

        print("HD queue is cleaned:", self.queue_hd_frame.empty())
        print("SD queue is cleaned:", self.queue_sd_frame.empty())
        
        print('Stopping Process Capture... ')
        if self.processCapture is not None:
            self.processCapture.join()

if __name__=='__main__':

    queue_frame_hd = Queue(maxsize=100)
    queue_frame_sd = Queue(maxsize=100)

    json_config = {}
    with open('../config.json', 'r') as json_file:
        json_config = json.load(json_file)

    IP = json_config['rtsp']['ip']
    PORT = json_config['rtsp']['port']
    USERNAME = json_config['rtsp']['username']
    PASSWORD = json_config['rtsp']['password']

    rtsp_stream = RTSPStream(ip=IP, port=PORT,
                             username=USERNAME, password=PASSWORD,
                             queue_hd=queue_frame_hd, queue_sd=queue_frame_sd)
    rtsp_stream.start()
    print('Start Successful!')
    
    start_time = time.time()
    while (time.time() - start_time) <= 30:
        
        hd_frame = queue_frame_hd.get()
        sd_frame = queue_frame_sd.get()
        
        # cv2.imshow('RTSP Streamming Result', hd_frame)
        cv2.imshow('RTSP Streamming Result', sd_frame)

        if cv2.waitKey(1) == 27:
            break
    
    cv2.destroyAllWindows()
    rtsp_stream.stop()    
    print('Stop Successful!')