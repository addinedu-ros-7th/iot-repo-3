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
import os
from VideoPopup import VideoPopup
from database import *


from_class = uic.loadUiType("./src/iot_project.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pixmap = QPixmap()

        # cascade xml 파일 선택
        self.body_cascade = cv2.CascadeClassifier('./data/haarcascade_fullbody.xml')
        self.face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')

        self.camera = iot_Thread(self)
        self.camera.daemon = True 
        self.camera.update.connect(self.updateCamera)
        self.isConveyor = False

        self.record = iot_Thread(self)
        self.record.daemon = True
        self.record.update.connect(self.updateRecording)
        self.isRecStart = False

        self.btnMonitoring.clicked.connect(self.clickMonitoring)
        self.btnControll.clicked.connect(self.clickControll)
        self.btnCCTV.clicked.connect(self.clickCCTV)

        self.mon_btn_state = False
        self.con_btn_state = False
        self.cct_btn_state = False

        self.cctvControll.hide()
        self.conveyorControll.hide()
        self.conveyorMonitoring.hide()

        self.conveyorStartButton.clicked.connect(self.startConveyor)
        self.conveyorStopButton.clicked.connect(self.stopConveyor)

        self.conveyorState = False
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

        # cctv window
        self.video_folder_path = 'data'
        
        # self.cctvLayout.setContentsMargins(0, 0, 0, 0)
        # self.cctvLayout.setSpacing(5)
        
        self.cctvOrderComboBox.addItems(["이름 오름차순", "이름 내림차순"])
        self.cctvOrderComboBox.setFixedWidth(150)  # 드롭다운 너비를 150으로 고정
        self.cctvOrderComboBox.setFixedHeight(30)
        self.cctvOrderComboBox.currentIndexChanged.connect(self.sort_buttons)

        self.cameraStatus = True
        self.cameraStart()

        # self.activeBarcord()

        self.pixmap1 = QPixmap()
        self.pixmap2 = QPixmap()
        self.pixmap3 = QPixmap()

        self.insertChart()

    def insertChart(self):
        self.image1 = cv2.imread('./data/chart_1.jpeg')
        self.image2 = cv2.imread('./data/chart_2.jpeg')
        self.image3 = cv2.imread('./data/chart_3.jpeg')

        # print("123", self.image2, "123")

        self.image1 = cv2.cvtColor(self.image1, cv2.COLOR_BGR2RGB)
        self.image2 = cv2.cvtColor(self.image2, cv2.COLOR_BGR2RGB)
        self.image3 = cv2.cvtColor(self.image3, cv2.COLOR_BGR2RGB)

        h, w, c, = self.image1.shape
        self.qimage1 = QImage(self.image1.data, w, h, w*c, QImage.Format_RGB888)
        self.pixmap1 = self.pixmap1.fromImage(self.qimage1)
        self.pixmap1 = self.pixmap1.scaled(self.chartLabel_1.width(), self.chartLabel_1.height())
        self.chartLabel_1.setPixmap(self.pixmap1)

        h, w, c, = self.image2.shape
        self.qimage2 = QImage(self.image2.data, w, h, w*c, QImage.Format_RGB888)
        self.pixmap2 = self.pixmap2.fromImage(self.qimage2)
        self.pixmap2 = self.pixmap2.scaled(self.chartLabel_2.width(), self.chartLabel_2.height())
        self.chartLabel_2.setPixmap(self.pixmap2)

        h, w, c, = self.image3.shape
        self.qimage3 = QImage(self.image3.data, w, h, w*c, QImage.Format_RGB888)
        self.pixmap3 = self.pixmap3.fromImage(self.qimage3)
        self.pixmap3 = self.pixmap3.scaled(self.chartLabel_3.width(), self.chartLabel_3.height())
        self.chartLabel_3.setPixmap(self.pixmap3)
        
        self.listGroup.setStyleSheet("""
            QGroupBox {
                background-color: #ADD8E6;  
                border: none;
                max-width: 220px;
            }

            QGroupBox::title {
                color: #FFFFFF;              
                background-color: #87CEFA;  
                padding: 5px;               
                text-align: center;
            }
            QLabel {
                background-color: #ADD8E6;  
                padding: 5px;               
            }
            QLabel:last-child {
                background-color: #FFB6C1;  
                color: #000000;            
            }

            QPushButton {
                width: 220px;                 
                height: 60px;                
                border: none;                 
                text-align: left;              
                padding: 0 10px;
            }
        """)

        self.cctvControll.setGeometry(240, 0, 800, 700)
        self.conveyorControll.setGeometry(240, 0, 800, 700)
        self.conveyorMonitoring.setGeometry(240, 0, 800, 700)

    def activeBarcord(self):
        # 시리얼 포트와 속도 설정
        self.serial_thread = SerialThread('/dev/ttyACM0', 9600)
        self.serial_thread.data_received.connect(self.update_label)
        self.serial_thread.start()  # 별도의 스레드에서 시리얼 통신 시작
    
    def update_label(self, data):
        # 시리얼 데이터를 받으면 라벨을 업데이트
        self.barcodeLabel.setText(f"Received: {data}")

    # visualization window functions
    def clickMonitoring(self):
        self.cctvControll.hide()
        self.conveyorControll.hide()
        self.conveyorMonitoring.show()

        self.mon_btn_state = not self.mon_btn_state

        if ( self.mon_btn_state == True ) :
            self.btnMonitoring.setStyleSheet("background-color: #E5C9C9;")
        else :
            self.btnMonitoring.setStyleSheet("background-color: #ADD8E6;")

        self.btnControll.setStyleSheet("background-color: #ADD8E6;")
        self.btnCCTV.setStyleSheet("background-color: #ADD8E6;")
    
    # conveyor controll window functions
    def clickControll(self):
        self.cctvControll.hide()
        self.conveyorControll.show()
        self.conveyorMonitoring.hide()

        self.con_btn_state = not self.con_btn_state

        if ( self.con_btn_state == True ) :
            self.btnControll.setStyleSheet("background-color: #E5C9C9;")
        else :
            self.btnControll.setStyleSheet("background-color: #ADD8E6;")

        self.btnMonitoring.setStyleSheet("background-color: #ADD8E6;") 
        self.btnCCTV.setStyleSheet("background-color: #ADD8E6;")
    


    def startConveyor(self):
        # self.isCameraOn = True
        self.isConveyor = True
        self.conveyorState = True
        
        if self.cameraStatus == False:
            self.cameraStart()
        else :
            pass

        if self.isRecStart == False:
            self.isRecStart = True
            self.recordingStart()
        
        self.labelConveoyStatus.setText("True")
        self.labelConveoyStatus.setStyleSheet("background-color: rgba(0, 255, 0, 128);")

        excute_query("INSERT INTO conveyor values(now(),1);")

    def stopConveyor(self):
        self.conveyorState = False
        # self.cameraStop()

        if self.isRecStart == True:
            self.isRecStart = False
            self.recordingstop()
        
        self.labelConveoyStatus.setText("False")
        self.labelConveoyStatus.setStyleSheet("background-color: rgba(255, 0, 0, 128);")  # 빨간색

        excute_query("INSERT INTO conveyor values(now(),0);")

    def updateConveyorSpeedLabel(self):
        current_speed = self.SliderConveyorSpeed.value()
        self.labelConveyorSpeed.setText(f"현재 속도: {current_speed}")

    def updateDateTime(self):
        now = datetime.datetime.now()
        self.labelConveyorDate.setText(now.strftime("%Y-%m-%d"))
        self.labelConveyorTime.setText(now.strftime("%H:%M:%S"))

    def clickCCTV(self):
        self.cctvControll.show()
        self.conveyorControll.hide()
        self.conveyorMonitoring.hide()

        self.cct_btn_state = not self.cct_btn_state

        if ( self.cct_btn_state == True ) :
            self.btnCCTV.setStyleSheet("background-color: #E5C9C9;")
        else :
            self.btnCCTV.setStyleSheet("background-color: #ADD8E6;")

        self.btnMonitoring.setStyleSheet("background-color: #ADD8E6;") 
        self.btnControll.setStyleSheet("background-color: #ADD8E6;")

        self.video_files = [f for f in os.listdir(self.video_folder_path) if f.endswith(('.mp4', '.avi', '.mov'))]
        self.create_buttons(self.video_files)

    def updateRecording(self):
        self.writer.write(cv2.cvtColor(self.frame, cv2.COLOR_RGB2BGR))

    def recordingStart(self):
        self.record.running = True
        self.record.start()

        self.now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = "./data/" + self.now + ".avi"
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')

        w = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.writer = cv2.VideoWriter(filename , self.fourcc, 20.0, (w, h))

    def recordingstop(self):
        self.record.running = False

        if self.isRecStart == True:
            self.writer.release()

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

            self.face = self.face_cascade.detectMultiScale(self.frame, 1.1, 10, minSize=(20, 20))

            for (x,y,w,h) in self.face :
                cv2.rectangle(self.frame,(x,y),(x+w,y+h),(0,0,255),3)

            h, w, c, = self.frame.shape
            self.qimage = QImage(self.frame.data, w, h, w*c, QImage.Format_RGB888)

            self.pixmap = self.pixmap.fromImage(self.qimage)
            # self.pixmap = self.pixmap.scaled(self.printCamera.width(), self.printCamera.height())

            if (self.isConveyor == True) :
                self.pixmap = self.pixmap.scaled(self.labelConveyorCamera.width(), self.labelConveyorCamera.height())
                self.labelConveyorCamera.setPixmap(self.pixmap)
            else :
                self.pixmap = self.pixmap.scaled(self.labelConveyorCamera.width(), self.labelConveyorCamera.height())
                self.labelConveyorCamera.setPixmap(self.pixmap)
    
    # cctv window functions
    def sort_buttons(self):
        selected_sort = self.cctvOrderComboBox.currentText()
        
        if selected_sort == "이름 오름차순":
            sorted_files = sorted(self.video_files)
        elif selected_sort == "이름 내림차순":
            sorted_files = sorted(self.video_files, reverse=True)
        else:
            sorted_files = self.video_files  # 기본 정렬
        
        self.create_buttons(sorted_files)
    
    def open_video_popup(self, video_path):
        # 비디오 팝업 창 생성
        self.popup = VideoPopup(video_path)
        self.popup.exec()
    
    def create_buttons(self, files):
        
        # 기존 버튼 제거
        for i in reversed(range(self.cctvLayout.count())):
            widget = self.cctvLayout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # 정렬된 파일 리스트에 따라 버튼 생성
        for idx, file in enumerate(files):
            button = QPushButton(file)
            button.setFixedSize(200, 200)
            full_path = os.path.join(self.video_folder_path, file)
            button.clicked.connect(lambda checked, v=full_path: self.open_video_popup(v))
            row = idx // 3
            col = idx % 3
            self.cctvLayout.addWidget(button, row, col)

class SerialThread(QThread):
    # 시리얼 데이터를 읽으면 이 시그널을 메인 스레드로 보냄
    data_received = pyqtSignal(str)

    def __init__(self, port, baudrate):
        super().__init__()
        self.ser = serial.Serial(port, baudrate, timeout=1)
    
    def run(self):
        while True:
            if self.ser.in_waiting > 0:
                data = self.ser.readline().decode('utf-8').strip()
                self.data_received.emit(data)  # 데이터를 메인 스레드로 보냄
            time.sleep(0.1)

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