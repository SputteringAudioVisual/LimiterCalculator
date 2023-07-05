import os
from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QSplashScreen

import sys
import time



## This class override the QLabel paintEvent method and allow us to write text over the image
class ImageWriter(QLabel):

    ## initialize the class and load the background image
    # @param text. string containing the text displayed in the splash. Default text: 'loading...'
    # @param image_path. String containing the path to the image displayed in the background
    def __init__(self, text, image_path):
        super().__init__()
        self.setText(text)
        self.image_path = image_path
        self.img = QImage(self.image_path)
        self.img1 = self.img.scaled(800, 400)

    ## method overriding the parent paintEvent method
    def paintEvent(self, e):

        # create the painter instance
        qp = QPainter()
        qp.begin(self)
        qp.drawImage(QPoint(), self.img1)

        # create the pen instance and set the text settings
        pen = QPen(Qt.black)
        pen.setWidth(1)
        qp.setPen(pen)
        font = QFont()
        font.setFamily('Times')
        font.setPointSize(12)
        qp.setFont(font)
        # write the text over the image with the drawText()  parent method
        qp.drawText(300, 580, self.text())


## this class creates a frameless window from parent class QMainWindow().
class SplashWindow(QMainWindow):

    ## Initialize the window and set characteristics as size, frameless borders, icons and widgets
    def __init__(self, resourcesPath=os.getcwd(), iconFile=r'/imgageFF.png', splashImFile=r'imgageFF.png'):
        super(SplashWindow, self).__init__()



        # set the size of the window
        self.setFixedSize(800, 400)

        # Remove the frames
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)

        # Set the icon associated to the window
        self.setWindowIcon(QIcon(str(resourcesPath + iconFile)))

        # Create an instance of the ImageWriter class
        self.central_widget = ImageWriter('Loading...', str(resourcesPath / Path(splashImFile)))
        self.central_widget.update()

        # display the ImageWriter instance as the central widget
        self.setCentralWidget(self.central_widget)

    ## This method allow to dynamically change the text on the imageWriter() instance
    # by calling the QLabel.setText() method
    def setText(self, new_text):
        self.central_widget.setText(new_text)


if __name__ == '__main__':


    app = QApplication(sys.argv)
    win = SplashWindow(iconFile=r'/img.png')
    win.show()
    win.setText('initializing camera systems')
    app.processEvents()
    time.sleep(3)
    win.setText('adios')
    app.processEvents()
    time.sleep(3)
    win.close()
    app.processEvents()
    time.sleep(1)
