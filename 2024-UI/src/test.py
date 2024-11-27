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

from_class = uic.loadUiType("./test.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.barcode = iot_Thread(self)
        self.barcode.daemon = True
        self.barcode.update.connect(self.updateBarcode)
        # self.dev = usb.core.find(idVendor=0x1234, idProduct=0x5678)
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.barcodeData = 0
        self.barcode.start()

    def updateBarcode(self):
        if self.ser.isOpen():
            self.read = self.ser.readline().decode('ascii')
            self.label.setText(str(self.read))
            if str(self.read) != "":
                print(str(self.read))
        elif not(self.ser.isOpen()):
            self.label.setText(str(None))

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