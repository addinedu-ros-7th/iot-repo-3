from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QGridLayout, QPushButton
#from PySide6.QtWidgets import QWidget, QVBoxLayout, QComboBox, QGridLayout, QPushButton
import os
from VideoPopup import VideoPopup

class CCTVTab(QWidget):
    def __init__(self, video_folder_path):
        super().__init__()
        
        # 비디오 파일 경로 설정
        self.video_folder_path = video_folder_path
        self.video_files = [f for f in os.listdir(self.video_folder_path) if f.endswith(('.mp4', '.avi', '.mov'))]

        # 레이아웃 구성
        main_layout = QVBoxLayout(self)  # 최상위 레이아웃
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(5)
        
        # 드롭다운 메뉴 추가
        self.sort_dropdown = QComboBox()
        self.sort_dropdown.addItems(["이름 오름차순", "이름 내림차순"])
        self.sort_dropdown.setFixedWidth(150)  # 드롭다운 너비를 150으로 고정
        self.sort_dropdown.setFixedHeight(30)
        self.sort_dropdown.currentIndexChanged.connect(self.sort_buttons)
        main_layout.addWidget(self.sort_dropdown)

        # 비디오 버튼을 위한 그리드 레이아웃
        self.grid_layout = QGridLayout()
        main_layout.addLayout(self.grid_layout)
        
        # 초기 버튼 생성
        self.create_buttons(self.video_files)
    
    def create_buttons(self, files):
        # 기존 버튼 제거
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
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
            self.grid_layout.addWidget(button, row, col)

    def sort_buttons(self):
        # 드롭다운 선택에 따라 정렬 방식 결정
        selected_sort = self.sort_dropdown.currentText()
        
        if selected_sort == "이름 오름차순":
            sorted_files = sorted(self.video_files)
        elif selected_sort == "이름 내림차순":
            sorted_files = sorted(self.video_files, reverse=True)
        else:
            sorted_files = self.video_files  # 기본 정렬

        # 버튼 재생성
        self.create_buttons(sorted_files)

    def open_video_popup(self, video_path):
        # 비디오 팝업 창 생성
        self.popup = VideoPopup(video_path)
        self.popup.exec()
