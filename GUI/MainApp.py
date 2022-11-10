from PyQt5.QtWidgets import QMainWindow, QGridLayout, QCheckBox, QFileDialog, QApplication
from PyQt5.uic import loadUi
import sys
from PyQt5 import QtCore
from amplifiers.AmplifierBase import amplifierBase
from Speakers.SpeakerBase import speakerBase
from LimiterAPI import LimiterAPI

class LimiterApp(QMainWindow):
    def __init__(self):
        super(LimiterApp, self).__init__()
        QMainWindow.__init__(self)
        loadUi(r'D:\Repositorios\LimiterCalculator\GUI\MainGUI.ui', self)
        self.setEnabled(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.show()

        self.amp = amplifierBase()
        self.driver = speakerBase()

        self.SpeakerImpedanceValue.setText(None)
        self.SpeakerPowerValue.setText(None)
        self.AmpImpedanceValue.setText(None)
        self.AmpPowerValue.setText(None)
        self.SensitivityValue.setText(None)
        self.RMSThresholdValue.setText('asdasdasdasda')
        self.PeakThresholdValue.setText(None)
        self.AttackValue.setText(None)
        self.ReleaseValue.setText(None)

        self.SpeakerImpedanceValue.setText(str(8))
        self.SpeakerPowerValue.setText(str(100))
        self.AmpImpedanceValue.setText(str(8))
        self.AmpPowerValue.setText(str(200))
        self.SensitivityValue.setText(str(1.2))
        self.RMSThresholdValue.setText(None)
        self.PeakThresholdValue.setText(None)
        self.AttackValue.setText(None)
        self.ReleaseValue.setText(None)

        self.RMSThresholdValue.setEnabled(False)
        self.PeakThresholdValue.setEnabled(False)
        self.AttackValue.setEnabled(False)
        self.ReleaseValue.setEnabled(False)

        self.ProtectionCombo.currentIndexChanged.connect(self.keyPressEvent)

        #inicializamos la API
        self.API = LimiterAPI()

        # Creamos variables vacias para evitar crashes
        self.Peak_TH =None
        self.RMS_TH =None




    def keyPressEvent(self, event):
        self.API.protect = float(self.ProtectionCombo.itemText(self.ProtectionCombo.currentIndex()))

        ValueList = [self.SpeakerImpedanceValue.text(), self.SpeakerPowerValue.text(), self.AmpImpedanceValue.text(),
                     self.AmpPowerValue.text(), self.SensitivityValue.text()]
        driverValues = [self.SpeakerImpedanceValue.text(), self.SpeakerPowerValue.text()]

        ampValues = [ self.AmpImpedanceValue.text(), self.AmpPowerValue.text(), self.SensitivityValue.text()]

        if '' not in set(driverValues):
           self.updateDriver(driverValues)
        else:
            pass

        if '' not in set(ampValues):
            self.updateAmp(ampValues)
        else:
            pass

        if '' not in set(ValueList):
            self.CalculateLimiters()
            self.updateGUIValues()

        else:
            pass

    def updateDriver(self, driver_values):
        self.driver.setImpedance(float(driver_values[0]))
        self.driver.setPower(float(driver_values[1]))
        self.driver.CalculateRMSPeakValues()
        self.API.setDriver(self.driver)
    def updateAmp(self, amp_values):
        self.amp.setImpedance(float(amp_values[0]))
        self.amp.setPower(float(amp_values[1]))
        self.amp.CalculateRMSPeakValues()
        self.amp.setVsens(float(amp_values[2]))
        self.API.setAmp(self.amp)

    def CalculateLimiters(self):
        self.API.calculatePeakLimiter()
        self.API.CalculateRMSLimiter()


    def updateGUIValues(self):
        if self.RMSThresholdUnitCombo.itemText(self.RMSThresholdUnitCombo.currentIndex())=='dBu':
            self.RMSThresholdValue.setText(str(self.API.RMS_dBuTH))
        else:
            self.RMSThresholdValue.setText('not implemented Yet')

        if self.PeakThresholdUnitCombo.itemText(self.PeakThresholdUnitCombo.currentIndex()) == 'dBu':
            self.PeakThresholdValue.setText(str(self.API.Peak_dBuTH))
        else:
            self.PeakThresholdValue.setText('not implemented Yet')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LimiterApp()
    app.exec_()