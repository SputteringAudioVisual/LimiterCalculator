from PyQt5.QtWidgets import QApplication
import sys
import qdarktheme
from GUI.MainGui.MainApp import LimiterApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = LimiterApp(splash=False)
    app.exec_()