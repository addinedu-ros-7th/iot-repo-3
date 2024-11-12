from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap

#from PySide6.QtCore import QThread, Signal, Qt
#from PySide6.QtGui import QImage, QPixmap
import cv2
import time

class Camera(QThread):
    #update = Signal()
    update = pyqtSignal()

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True

        # cascade xml 파일 선택
        self.body_cascade = cv2.CascadeClassifier('../data/haarcascade_fullbody.xml')
        self.face_cascade = cv2.CascadeClassifier('../data/haarcascade_frontalface_default.xml')

    def run(self):
        while self.running:
            self.update.emit()  # 프레임 갱신 신호 발행
            time.sleep(0.1)

    def stop(self):
        self.running = False

    def updateThread(self, video, display, err_msg):
        retval, self.image = video.read()

        if retval:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

            # 10 = 검출한 사각형 사이 최소 간격, body에 x,y,w,h가 여러개 저장됨.
            self.body = self.body_cascade.detectMultiScale(self.image, 1.1, 10, minSize=(20, 20))

            for (x,y,w,h) in self.body :         
                cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,0,255),3)

            self.face = self.face_cascade.detectMultiScale(self.image, 1.1, 10, minSize=(20, 20))

            for (x,y,w,h) in self.face :
                cv2.rectangle(self.image,(x,y),(x+w,y+h),(0,0,255),3)

            h, w, c = self.image.shape
            qimage = QImage(self.image.data, w, h, w * c, QImage.Format_RGB888)
            self.pixmap = QPixmap.fromImage(qimage)
            self.pixmap = self.pixmap.scaled(
                display.width(),
                display.height(),
                Qt.KeepAspectRatio
            )
            display.setPixmap(self.pixmap)
        else:
            display.setText(err_msg)
