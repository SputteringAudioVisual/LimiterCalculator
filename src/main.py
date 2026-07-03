import sys
from pathlib import Path

# Ensure the project root is on sys.path regardless of working directory
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PyQt5.QtWidgets import QApplication
import qdarktheme
from GUI.MainGui.MainApp import LimiterApp


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = LimiterApp(splash=False)
    app.exec_()
