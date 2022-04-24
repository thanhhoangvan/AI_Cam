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
import face_recognition
import matplotlib.pyplot as plt


class FaceID:
    def __init__(self):
        self.ListFaceName = []
        self.ListEncodeFace = []

    def getFaceLocation(self, image):
        return face_recognition.face_locations(image)[0]
    
    def getFaceEncode(self, image):
        return face_recognition.face_encodings(image)[0]
    
    def addNewFace(self, image, name="Unknow"):
        self.ListFaceName.append(name)
        self.ListEncodeFace.append(self.getFaceEncode(image))
        return
    
    def recognition(self, image):
        FaceEncoded = self.getFaceEncode(image)
        for FaceID in range(len(self.ListEncodeFace)):
            result = face_recognition.compare_faces([self.ListEncodeFace[FaceID]], FaceEncoded)
            if result:
                return self.ListFaceName[FaceID]
    
    def show(self, image):
        pass
    
    def deleteFace(self, name="Unknow"):
        for faceid in range(len(self.ListFaceName)):
            if self.ListFaceName[faceid] == name:
                self.ListFaceName.remove(name)
                del self.ListEncodeFace[faceid:faceid+1]
                break

if __name__=='__main__':
    pass