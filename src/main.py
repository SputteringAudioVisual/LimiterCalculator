from PyQt5.QtWidgets import QApplication
import sys

from GUI.MainGui.MainApp import LimiterApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LimiterApp()
    app.exec_()