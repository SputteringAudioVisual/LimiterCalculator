from PyQt5.QtWidgets import QMainWindow, QMessageBox, QCheckBox, QFileDialog, QApplication
from PyQt5.uic import loadUi
import sys
import os
from pathlib import Path
from PyQt5 import QtCore
from amplifiers.AmplifierBase import amplifierBase
from Speakers.SpeakerBase import speakerBase
from src.API.LimiterAPI import LimiterAPI
import json


class LimiterApp(QMainWindow):
    def __init__(self):
        super(LimiterApp, self).__init__()
        QMainWindow.__init__(self)
        print(os.getcwd())
        loadUi(Path(os.getcwd()).parent / Path('GUI/MainGUI/MainGUI_new.ui'), self)
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
        self.RMSThresholdValue.setText(None)
        self.PeakThresholdValue.setText(None)
        self.AttackValue.setText(None)
        self.ReleaseValue.setText(None)

        self.RMSThresholdValue.setText(None)
        self.PeakThresholdValue.setText(None)
        self.AttackValue.setText(None)
        self.ReleaseValue.setText(None)
        self.HPFValue.setText(None)

        self.ValueList = [self.SpeakerImpedanceValue.text(), self.SpeakerPowerValue.text(),
                          self.AmpImpedanceValue.text(), self.AmpPowerValue.text(),
                          self.SensitivityValue.text(), self.HPFValue.text()]

        self.outputTable.resizeColumnsToContents()



        self.RMSThresholdValue.setEnabled(False)
        self.PeakThresholdValue.setEnabled(False)
        self.AttackValue.setEnabled(False)
        self.ReleaseValue.setEnabled(False)
        self.SpeakerImpedanceLabel.setEnabled(True)
        self.SpeakerPowerLabel.setEnabled(True)
        self.loadDriverButton.setEnabled(True)
        self.loadAmpButton.setEnabled(True)
        self.OperationMode.hide()
        self.AmpImpedanceComBoBox.hide()

        self.ProtectionCombo.currentIndexChanged.connect(self.keyPressEvent)
        self.RMSThresholdUnitCombo.currentIndexChanged.connect(self.keyPressEvent)
        self.PeakThresholdUnitCombo.currentIndexChanged.connect(self.keyPressEvent)

        self.loadAmpButton.clicked.connect(self.openAmpDialog)
        self.loadDriverButton.clicked.connect(self.openDriverDialog)
        self.AmpImpedanceComBoBox.currentIndexChanged.connect(self.keyPressEvent)
        self.OperationMode.currentIndexChanged.connect(self.changeAmpConfiguration)
        self.SensitivityUnitCombo.currentIndexChanged.connect(self.keyPressEvent)

        #inicializamos la API
        self.API = LimiterAPI()

        # Creamos variables vacias para evitar crashes
        self.Peak_TH =None
        self.RMS_TH =None
        self.driverData = None
        self.allNumericValues = False




    def keyPressEvent(self, event):
        if self.AmpImpedanceComBoBox:
            self.AmpImpedanceValue.setText(self.AmpImpedanceComBoBox.currentText())
            self.AmpPowerValue.setText(str(self.AmpData[self.OperationMode.currentText()]['Power'][self.AmpImpedanceComBoBox.currentIndex()]))
            self.SensitivityValue.setText(str(self.AmpData['Sensitivity'][self.SensitivityUnitCombo.currentText()]))

        NewValueList = [self.SpeakerImpedanceValue.text(), self.SpeakerPowerValue.text(), self.AmpImpedanceValue.text(),
                     self.AmpPowerValue.text(), self.SensitivityValue.text(), self.HPFValue.text()]




        for value, newValue in zip(self.ValueList, NewValueList) :
            if value!=newValue:
                try:
                    float(newValue)
                    self.allNumericValues =True
                except:
                    self.allNumericValues = False

        self.ValueList = [self.SpeakerImpedanceValue.text(), self.SpeakerPowerValue.text(), self.AmpImpedanceValue.text(),
                     self.AmpPowerValue.text(), self.SensitivityValue.text(), self.HPFValue.text()]


        driverValues = [self.SpeakerImpedanceValue.text(), self.SpeakerPowerValue.text()]

        ampValues = [ self.AmpImpedanceValue.text(), self.AmpPowerValue.text(), self.SensitivityValue.text(), self.HPFValue.text()]

        if self.allNumericValues:
            self.API.protect = float(self.ProtectionCombo.itemText(self.ProtectionCombo.currentIndex()))

            if self.HPFValue.text():
                self.API.setHPF(float(self.HPFValue.text()))

            if '' not in set(driverValues):
               self.updateDriver(driverValues)
            else:
                pass

            if '' not in set(ampValues):
                self.updateAmp(ampValues)
            else:
                pass

            if '' not in set(self.ValueList):
                self.CalculateLimiters()
                self.updateGUIValues()
            else:
                pass
        else:
            QMessageBox.warning(self, 'WARNING!',
                                    'Please use only numerical values.',
                                    QMessageBox.Ok)

    def updateDriver(self, driver_values):
        self.driver.setImpedance(float(driver_values[0]))
        self.driver.setPower(float(driver_values[1]))
        self.driver.CalculateRMSPeakValues()
        self.API.setDriver(self.driver)

    def updateAmp(self, amp_values):
        self.amp.setImpedance(float(amp_values[0]))
        self.amp.setPower(float(amp_values[1]))
        self.amp.CalculateRMSPeakValues()

        if self.SensitivityUnitCombo.itemText(self.SensitivityUnitCombo.currentIndex())=='V sens':
            self.amp.setVsens(float(amp_values[2]))
        if self.SensitivityUnitCombo.itemText(self.SensitivityUnitCombo.currentIndex()) == 'dBu sens':
            self.amp.setDBUSens(float(amp_values[2]))
        if self.SensitivityUnitCombo.itemText(self.SensitivityUnitCombo.currentIndex()) == 'X Factor':
            self.amp.setXfactor(float(amp_values[2]))
        self.API.setAmp(self.amp)

    def CalculateLimiters(self):
        self.API.calculatePeakLimiter()
        self.API.CalculateRMSLimiter()
        self.API.calculateTimeParameters()

    def changeAmpConfiguration(self):
        impedanceList = [str(impedance) for impedance in self.AmpData[self.OperationMode.currentText()]['Impedance']]
        self.AmpImpedanceComBoBox.clear()
        self.AmpImpedanceComBoBox.addItems(impedanceList)


    def updateGUIValues(self):
        self.AttackValue.setText(str(self.API.attack))
        self.ReleaseValue.setText(str(self.API.release))

        if self.RMSThresholdUnitCombo.itemText(self.RMSThresholdUnitCombo.currentIndex())=='dBu':
            self.RMSThresholdValue.setText(str(round(self.API.RMS_dBuTH, 2)))
        elif self.RMSThresholdUnitCombo.itemText(self.RMSThresholdUnitCombo.currentIndex()).split()[0] == 'dBfs':
            self.RMSThresholdValue.setText(str(round(self.API.RMS_dBuTH-22 ,2)))
        else:
            self.RMSThresholdValue.setText('not implemented Yet')

        if self.PeakThresholdUnitCombo.itemText(self.PeakThresholdUnitCombo.currentIndex()) == 'dBu':
            self.PeakThresholdValue.setText(str(round(self.API.Peak_dBuTH, 2)))
        elif self.PeakThresholdUnitCombo.itemText(self.PeakThresholdUnitCombo.currentIndex()).split()[0] == 'dBfs':
            self.PeakThresholdValue.setText(str(round(self.API.Peak_dBuTH-22, 2)))
        else:
            self.PeakThresholdValue.setText('not implemented Yet')


        self.RMSThresholdValue.setEnabled(True)
        self.PeakThresholdValue.setEnabled(True)
        self.AttackValue.setEnabled(True)
        self.ReleaseValue.setEnabled(True)
        self.RMSThresholdValue.setReadOnly(True)
        self.PeakThresholdValue.setReadOnly(True)
        self.AttackValue.setReadOnly(True)
        self.ReleaseValue.setReadOnly(True)


    def openAmpDialog(self):
        """!
        This method open a dialog to load a .pkl file on the GUI.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        driverDB = str(Path(os.getcwd()).parent) + r'\dataBase\amplifierDataBase'

        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", directory = driverDB,
                                                       initialFilter = "All Files (*);;amp file (*.json)", options=options)
        if self.fileName:

            with open(self.fileName, 'r') as f:
                self.AmpImpedanceComBoBox.show()
                self.OperationMode.show()

                self.AmpData = json.load(f)
                self.AmpImpedanceValue.setEnabled(False)
                self.AmpImpedanceValue.hide()
                self.AmpPowerValue.setEnabled(False)
                self.SensitivityValue.setEnabled(False)
                self.AmplificationInfoLabel.setText('AmpData Data:  ' + self.AmpData['Brand'] + '-' + self.AmpData['Model'])

                # show combo box with loaded data
                impedanceList = [str(impedance) for impedance in self.AmpData[self.OperationMode.currentText()]['Impedance']]
                self.AmpImpedanceComBoBox.clear()
                self.AmpImpedanceComBoBox.addItems(impedanceList)


            return True
        else:
            return False

    def openDriverDialog(self):
        """!
        This method open a dialog to load a .pkl file on the GUI.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        driverDB = str(Path(os.getcwd()).parent) + r'\dataBase\driverDataBase'
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", directory = driverDB,
                                                       initialFilter = "All Files (*);;driver file (*.json)", options=options)
        if self.fileName:
            with open(self.fileName, 'r') as f:
                self.DriverData = json.load(f)
                self.driver.setPower(self.DriverData['Power'])
                self.SpeakerPowerValue.setText(self.driver.power)
                self.SpeakerPowerValue.setEnabled(False)

                self.driver.setImpedance(self.DriverData['Impedance'])
                self.SpeakerImpedanceValue.setText(self.driver.impedance)
                self.SpeakerImpedanceValue.setEnabled(False)

                self.SpeakerInfoLabel.setText('Driver Data:  ' + self.DriverData['Brand'] + '-' + self.DriverData['Model'])
            return True
        else:
            return False

    def storeParams(self):
        pass
    def resetParams(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LimiterApp()
    app.exec_()