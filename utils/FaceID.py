"""
+============================================================+
- Tác Giả: Hoàng Thành
- Viện Toán Ứng dụng và Tin học(SAMI - HUST)
- Email: thanh.hoangvan051199@gmail.com
- Github: https://github.com/thanhhoangvan
+============================================================+
"""

import time
import face_recognition


class FaceID:
    def __init__(self):
        self.ListFaceName = []
        self.ListEncodeFace = []

    def getFaceLocation(self, image):
        return face_recognition.face_locations(image)
    
    def getFaceEncode(self, image):
        return face_recognition.face_encodings(image)
    
    def addNewFace(self, image, name="Unknow"):
        self.ListFaceName.append(name)
        self.ListEncodeFace.append(self.getFaceEncode(image))
        return
    
    def recognition(self, image):
        FaceEncoded = self.getFaceEncode(image)
        Faces = []
        if len(FaceEncoded) < 1:
            return None
        for FaceID in range(len(self.ListEncodeFace)):
            for face in FaceEncoded:
                result = face_recognition.compare_faces([self.ListEncodeFace[FaceID]], face)
                if result:
                    Faces.append(self.ListFaceName[FaceID])
        return Faces

    def loadListFaceID(self):
        pass

    def createFaceID(self):
        pass

    def saveListFaceID(self):
        pass
    
    def deleteFace(self, name="Unknow"):
        for faceid in range(len(self.ListFaceName)):
            if self.ListFaceName[faceid] == name:
                self.ListFaceName.remove(name)
                del self.ListEncodeFace[faceid:faceid+1]
                break

if __name__=='__main__':
    pass