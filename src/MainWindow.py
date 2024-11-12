import os
#from PySide6.QtCore import Qt
#from PySide6.QtWidgets import QWidget, QTabWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTabWidget, QLabel, QVBoxLayout, QGridLayout, QPushButton, QComboBox
import cv2
from Camera import Camera
from VideoPopup import VideoPopup
from CCTVTab import CCTVTab

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # QTabWidget 생성
        self.tab_widget = QTabWidget()
        
        # 첫 번째 탭: QLabel 추가
        self.home_tab = QWidget()
        home_layout = QVBoxLayout()
        self.home_label = QLabel()
        home_layout.addWidget(self.home_label)
        self.home_tab.setLayout(home_layout)
        
        # 두 번째 탭: 여러 개의 QPushButton 추가
        self.cctv_tab = CCTVTab("2024-UI/data")
        
        # 탭 위젯에 두 개의 탭 추가s
        self.tab_widget.addTab(self.home_tab, "Home")
        self.tab_widget.addTab(self.cctv_tab, "CCTV")
        
        # 메인 레이아웃에 QTabWidget 추가
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        self.setLayout(main_layout)

        # 카메라 초기화
        self.video = cv2.VideoCapture(0)

        # 카메라 쓰레드 설정 및 시작
        self.cameraThread = Camera()
        self.cameraThread.update.connect(lambda: self.cameraThread.updateThread(
            video=self.video, 
            display=self.home_label, 
            err_msg="카메라가 인식되지 않았어요ㅠ"))
        self.cameraThread.running = True
        self.cameraThread.start()


    def closeEvent(self, event):
        # 프로그램 종료 시 카메라 쓰레드 종료
        self.cameraThread.stop()
        self.video.release()
        event.accept()

