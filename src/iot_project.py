import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
import cv2, imutils
import time 
import datetime
import serial
import numpy as np
from matplotlib import pyplot as plt

from_class = uic.loadUiType("iot_project.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.led = -1
        self.dataFlow = 1 # PyQt와 아두이노 중 어느쪽이 데이터를 보내야하는지 결정하는 변수
        self.isCameraOn = False

        self.pixmap = QPixmap()

        # cascade xml 파일 선택
        self.body_cascade = cv2.CascadeClassifier('../data/haarcascade_fullbody.xml')
        self.face_cascade = cv2.CascadeClassifier('../data/haarcascade_frontalface_default.xml')

        self.camera = iot_Thread(self)
        self.camera.daemon = True 
        self.camera.update.connect(self.updateCamera)
        self.isConveyor = False

        self.btnLed.clicked.connect(self.btnClicked)
        self.btnCamera.clicked.connect(self.clickCamera)

        self.record = iot_Thread(self)
        self.record.daemon = True
        self.record.update.connect(self.updateRecording)
        self.isRecStart = False
        self.btnRecord.hide()
        self.btnRecord.clicked.connect(self.clickRecord)

        self.btnMonitoring.clicked.connect(self.clickMonitoring)
        self.btnControll.clicked.connect(self.clickControll)
        self.btnCCTV.clicked.connect(self.clickCCTV)

        self.cctvControll.hide()
        self.conveyorControll.hide()
        self.conveyorMonitoring.hide()

        self.cctvControll.setGeometry(240, 0, 800, 700)
        self.conveyorControll.setGeometry(240, 0, 800, 700)
        self.conveyorMonitoring.setGeometry(240, 0, 800, 700)

        self.conveyorStartButton.clicked.connect(self.startConveyor)
        self.conveyorStopButton.clicked.connect(self.stopConveyor)

        self.conveyorState = False
        # self.updateConveyorStatusLabel()
        self.SliderConveyorSpeed.valueChanged.connect(self.updateConveyorSpeedLabel)

        # date timer 
        self.updateDateTime()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)

        # Conveyor Window Slider Settings
        self.SliderConveyorSpeed.setValue(10)
        self.SliderConveyorSpeed.setMinimum(0)
        self.SliderConveyorSpeed.setMaximum(100)
        self.SliderConveyorSpeed.setSingleStep(10)

        self.conveyorStatusTitle.setText("컨베이어 시스템 현황")
        self.labelConveyorSpeed.setText("현재 속도: 10")


    def clickMonitoring(self):
        self.cctvControll.hide()
        self.conveyorControll.hide()
        self.conveyorMonitoring.show()

    def clickControll(self):
        self.cctvControll.hide()
        self.conveyorControll.show()
        self.conveyorMonitoring.hide()

    def startConveyor(self):
        self.isCameraOn = True
        self.isConveyor = True
        self.conveyorState = True
        self.cameraStart()

        if self.isRecStart == False:
            self.isRecStart = True
            self.recordingStart()
        
        self.labelConveoyStatus.setText("True")
        self.labelConveoyStatus.setStyleSheet("background-color: rgba(0, 255, 0, 128);") 

    def stopConveyor(self):
        self.isCameraOn = False
        self.conveyorState = False
        self.cameraStop()

        if self.isRecStart == True:
            self.isRecStart = False
            self.recordingstop()
        
        self.labelConveoyStatus.setText("False")
        self.labelConveoyStatus.setStyleSheet("background-color: rgba(255, 0, 0, 128);")  # 빨간색
    
    def updateConveyorSpeedLabel(self):
        current_speed = self.SliderConveyorSpeed.value()
        self.labelConveyorSpeed.setText(f"현재 속도: {current_speed}")

    def updateDateTime(self):
        now = datetime.datetime.now()
        self.labelConveyorDate.setText(now.strftime("%Y-%m-%d"))
        self.labelConveyorTime.setText(now.strftime("%H:%M:%S"))

    # def updateConveyorStatusLabel(self):
    #     if self.conveyorState:
    #         self.labelConveoyStatus.setText("True")
    #         self.labelConveoyStatus.setStyleSheet("background-color: rgba(0, 255, 0, 128);")  # 초록색
    #     else:
    #         self.labelConveoyStatus.setText("False")
    #         self.labelConveoyStatus.setStyleSheet("background-color: rgba(255, 0, 0, 128);")  # 빨간색

        # self.conveyorStartButton.clicked.connect(self.startConveyor)
        # self.conveyorStopButton.clicked.connect(self.stopConveyor)

    def clickCCTV(self):
        self.cctvControll.show()
        self.conveyorControll.hide()
        self.conveyorMonitoring.hide()

    def updateRecording(self):
        self.writer.write(cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))

    def recordingStart(self):
        self.record.running = True
        self.record.start()

        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = "../data/" + self.now + ".avi"
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.writer = cv2.VideoWriter(filename , self.fourcc, 20.0, (w, h))

    def recordingstop(self):
        self.record.running = False

        if self.isRecStart == True:
            self.writer.release()

    def clickRecord(self):
        if self.isRecStart == False:
            self.btnRecord.setText('Rec Stop')
            self.isRecStart = True

            self.recordingStart()
        else:
            self.btnRecord.setText('Rec Start')
            self.isRecStart = False

            self.recordingstop()

    def clickCamera(self):
        if self.isCameraOn == False:
            self.btnCamera.setText('Camera Off')
            self.isCameraOn = True
            self.btnRecord.show()

            self.cameraStart()
        else :
            self.btnCamera.setText('Camera On')
            self.isCameraOn = False
            self.btnRecord.hide()

            self.cameraStop()
            self.recordingstop()

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
            x = 0
            y = 0
            w = 0
            h = 0
            # grayImage1 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            # 10 = 검출한 사각형 사이 최소 간격, body에 x,y,w,h가 여러개 저장됨.
            # self.body = self.body_cascade.detectMultiScale(grayImage1, 1.1, 10, minSize=(10, 10))
            # self.body = self.body_cascade.detectMultiScale(self.frame, 1.1, 10, minSize=(20, 20))

            # for (x,y,w,h) in self.body :         
            #     cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,0,255),3)

            self.face = self.face_cascade.detectMultiScale(self.frame, 1.1, 10, minSize=(20, 20))

            for (x,y,w,h) in self.face :
                cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,0,255),3)
                # self.face_x.setText(str(x))
                # self.face_y.setText(str(y))
                # self.face_w.setText(str(w))
                # self.face_h.setText(str(h))
                # time.sleep(0.25)

            # print(x, y, w, h)

            h, w, c, = self.frame.shape
            self.qimage = QImage(self.frame.data, w, h, w*c, QImage.Format_RGB888)

            self.pixmap = self.pixmap.fromImage(self.qimage)
            # self.pixmap = self.pixmap.scaled(self.printCamera.width(), self.printCamera.height())

            if ( self.isConveyor == True ) :
                self.pixmap = self.pixmap.scaled(self.labelConveyorCamera.width(), self.labelConveyorCamera.height())
                self.labelConveyorCamera.setPixmap(self.pixmap)
            else :
                self.pixmap = self.pixmap.scaled(self.printCamera.width(), self.printCamera.height())
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