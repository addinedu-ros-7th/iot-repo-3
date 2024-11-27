#from PySide6.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
import cv2
from Camera import Camera

class VideoPopup(QDialog):
    def __init__(self, video_path):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.setFixedSize(640, 480)

        layout = QVBoxLayout(self)

        # QLabel을 사용하여 동영상 출력
        self.video_label = QLabel(self)
        self.video_label.setFixedSize(640, 480)
        layout.addWidget(self.video_label)

        # 일시 정지, 재생 버튼
        button_layout = QHBoxLayout()
        self.play_pause_button = QPushButton("일시 정지", self)
        self.play_pause_button.clicked.connect(self.toggle_play_pause)
        button_layout.addWidget(self.play_pause_button)
        layout.addLayout(button_layout)

        # 비디오 경로 설정
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        
        self.cameraThread = Camera()
        self.cameraThread.update.connect(lambda: self.cameraThread.updateThread(
            video=self.cap, 
            display=self.video_label, 
            err_msg="비디오가 인식되지 않았어요ㅠ"))
        self.cameraThread.running = True
        self.cameraThread.start()

        self.is_playing = True

    def toggle_play_pause(self):
        if self.is_playing:
            self.cameraThread.stop()
            self.play_pause_button.setText("재생")
        else:
            self.cameraThread.running = True
            self.cameraThread.start()
            self.play_pause_button.setText("일시 정지")
        self.is_playing = not self.is_playing


    def closeEvent(self, event):
        # 팝업 닫을 때 자원 해제
        self.cameraThread.stop()
        self.cap.release()
        event.accept()
