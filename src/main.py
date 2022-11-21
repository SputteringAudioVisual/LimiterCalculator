from PyQt5.QtWidgets import QMainWindow, QGridLayout, QCheckBox, QFileDialog, QApplication
from PyQt5.uic import loadUi
import sys
from PyQt5 import QtCore
from amplifiers.AmplifierBase import amplifierBase
from Speakers.SpeakerBase import speakerBase
from GUI.MainApp import LimiterApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LimiterApp()
    app.exec_()