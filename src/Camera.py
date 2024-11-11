from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QImage, QPixmap
import cv2
import time

class Camera(QThread):
    update = Signal()

    def __init__(self, sec=0, parent=None):
        super().__init__()
        self.main = parent
        self.running = True

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
