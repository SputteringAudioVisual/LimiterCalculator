from PyQt5.QtWidgets import QMainWindow, QGridLayout, QCheckBox, QFileDialog, QApplication
from PyQt5.uic import loadUi
import sys
from PyQt5 import QtCore
from amplifiers.AmplifierBase import amplifierBase
from Speakers.SpeakerBase import speakerBase

class LimiterApp(QMainWindow):
    def __init__(self):
        super(LimiterApp, self).__init__()
        QMainWindow.__init__(self)
        loadUi(r'D:\Repositorios\LimiterCalculator\GUI\MainGUI.ui', self)
        self.setEnabled(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.show()

        self.amp = amplifierBase
        self.driver = speakerBase

        self.SpeakerImpedanceValue.setText(None)
        self.SpeakerPowerValue.setText(None)
        self.AmpImpedanceValue.setText(None)
        self.AmpPowerValue.setText(None)
        self.SensitivityValue.setText(None)
        self.RMSThresholdValue.setText(None)
        self.PeakThresholdValue.setText(None)
        self.AttackValue.setText(None)
        self.ReleaseValue.setText(None)

        self.RMSThresholdValue.setEnabled(False)
        self.PeakThresholdValue.setEnabled(False)
        self.AttackValue.setEnabled(False)
        self.ReleaseValue.setEnabled(False)




    def RefreshValues(self):
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LimiterApp()
    app.exec_()