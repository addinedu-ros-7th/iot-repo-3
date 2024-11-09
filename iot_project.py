import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import cv2, imutils
import time 
import datetime
import serial

from_class = uic.loadUiType("iot_project.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.led = -1
        self.dataFlow = 1 # PyQt와 아두이노 중 어느쪽이 데이터를 보내야하는지 결정하는 변수

        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

        self.btnLed.clicked.connect(self.btnClicked)

        self.crossing_data = iot_Thread(self)
        self.crossing_data.daemon = True
        self.crossing_data.update.connect(self.updateData)
        self.crossing_data.start()

        self.ser.write(f"{self.led}\n".encode())

        self.camera = iot_Thread(self)
        self.camera.daemon = True
        self.camera.update.connect(self.updateCamera)
        self.btnCamera.clicked.connect(self.clickCamera)

    def clickCamera(self):
        if self.isCameraOn == False:
            self.btnCamera.setText('Camera Off')
            self.isCameraOn = True
            self.cameraStart()
        else :
            self.btnCamera.setText('Camera On')
            self.isCameraOn = False
            self.cameraStop()

    def cameraStart(self):
        self.camera.running = True
        self.camera.start()
        self.video = cv2.VideoCapture(-1)

    def cameraStop(self):
        self.camera.running = False
        self.count = 0
        self.video.release()

        if self.isRecStart == True:
            self.writer.release()

    def updateCamera(self):
        retval, self.frame = self.video.read()
        if retval:
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  

            h, w, c, = self.frame.shape
            self.qimage = QImage(self.frame.data, w, h, w*c, QImage.Format_RGB888)

            self.pixmap = self.pixmap.fromImage(self.qimage)
            self.pixmap = self.pixmap.scaled(self.label.width(), self.label.height())

            self.printCamera.setPixmap(self.pixmap)

    def updateData(self):
        if self.dataFlow == 1:
            if self.ser.in_waiting:
                self.lightSensor.setText(self.ser.readline().decode())
                self.dataFlow *= -1
        elif self.dataFlow == -1:
            self.dataFlow *= -1
            self.ser.write(f"{self.led}\n".encode())
        
        time.sleep(0.1)
        

    def btnClicked(self):
        self.led *= -1

class iot_Thread(QThread):
    update = pyqtSignal()

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True

    def run(self):
        count = 0
        while self.running == True:
            self.update.emit()
            time.sleep(0.1)
        
    def stop(self):
        self.running = False

if __name__=="__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec_())