from PyQt5.QtWidgets import QMainWindow, QMessageBox, QFileDialog, QApplication, QTableWidgetItem, QSplashScreen
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap, QFont
import sys
import os
from PyQt5.QtCore import Qt
from pathlib import Path
from PyQt5 import QtCore
from amplifiers.AmplifierBase import amplifierBase
from Speakers.SpeakerBase import speakerBase
from src.API.LimiterAPI import LimiterAPI
import json
import time

_HERE = Path(__file__).resolve().parent      # .../GUI/MainGui
_GUI_DIR = _HERE.parent                      # .../GUI
_ROOT = _GUI_DIR.parent                      # project root

# Items shown in SensitivityUnitCombo when in manual (Custom) mode
_SENS_UNITS_DEFAULT = ['V sens', 'dBu sens', 'X Factor', 'DB']

# JSON top-level keys that are NOT operating modes
_AMP_META_KEYS = {'Brand', 'Model', 'Sensitivity'}

# Default OperationMode items when in Custom (manual) mode
_OP_MODES_DEFAULT = ['Stereo', 'Bridge']


def _db_root() -> Path:
    """En frozen, busca dataBase/ junto al .exe primero (editable por el usuario)."""
    if getattr(sys, 'frozen', False):
        candidate = Path(sys.executable).parent / 'dataBase'
        if candidate.exists():
            return Path(sys.executable).parent
    return _ROOT


class LimiterApp(QMainWindow):
    def __init__(self, splash=False):
        imgPath = _GUI_DIR / 'resources' / 'imageFF.png'
        backImage = QPixmap(str(imgPath))
        textFont = QFont()
        textFont.setFamily('Times')
        textFont.setPointSize(12)

        if splash:
            self.splash = QSplashScreen(backImage)
            self.splash.setFont(textFont)
            self.splash.showMessage('', Qt.AlignCenter | Qt.AlignBottom, color=Qt.white)
            self.splash.show()
            time.sleep(4)
            self.splash.close()

        super(LimiterApp, self).__init__()
        loadUi(_HERE / 'MainGUI.ui', self)
        self.setEnabled(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.show()

        self.amp = amplifierBase()
        self.driver = speakerBase()

        for field in [self.SpeakerImpedanceValue, self.SpeakerPowerValue,
                      self.AmpImpedanceValue, self.AmpPowerValue,
                      self.SensitivityValue, self.RMSThresholdValue,
                      self.PeakThresholdValue, self.AttackValue,
                      self.ReleaseValue, self.HPFValue]:
            field.setText('')

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
        self.StoreParamsButton.setEnabled(False)
        self.outputTable.setAlternatingRowColors(True)
        self.OperationMode.hide()
        self.AmpImpedanceComBoBox.hide()

        # Sensitivity state — unit is tracked separately from combo text (DB mode)
        self.currentSensUnit = 'V sens'
        self.SensitivityOptions = []   # list of {label, unit, value} when amp loaded from JSON

        # Combo signals
        self.ProtectionCombo.currentIndexChanged.connect(self._recalculate)
        self.RMSThresholdUnitCombo.currentIndexChanged.connect(self._recalculate)
        self.PeakThresholdUnitCombo.currentIndexChanged.connect(self._recalculate)
        self.AmpImpedanceComBoBox.currentIndexChanged.connect(self._recalculate)
        self.SensitivityUnitCombo.currentIndexChanged.connect(self._on_sensitivity_combo_changed)
        self.OperationMode.currentIndexChanged.connect(self.changeAmpConfiguration)

        # Text field signals — editingFinished fires on Enter or focus-out
        for field in [self.SpeakerImpedanceValue, self.SpeakerPowerValue,
                      self.AmpImpedanceValue, self.AmpPowerValue,
                      self.SensitivityValue, self.HPFValue, self.LPFValue]:
            field.editingFinished.connect(self._recalculate)

        self.loadAmpButton.clicked.connect(self.openAmpDialog)
        self.loadDriverButton.clicked.connect(self.openDriverDialog)
        self.DeleteInputDataButton.clicked.connect(self.resetParams)
        self.StoreParamsButton.clicked.connect(self.storeParams)

        self.API = LimiterAPI()

        self.driveType = 'Custom'
        self.ampType = 'Custom'
        self.Peak_TH = None
        self.RMS_TH = None
        self.driverData = None
        self.allNumericValues = False
        self.row = 0

    # ------------------------------------------------------------------
    # Sensitivity helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _load_sensitivity_options(sens_data):
        """Convert JSON Sensitivity field to list of {label, unit, value}.

        Accepts both the new list format and the old dict format for
        backward compatibility with hand-edited JSON files.
        """
        if isinstance(sens_data, list):
            return sens_data
        # Old dict format: {"V sens": 0.775, "dBu sens": 0.0, "X Factor": false}
        options = []
        for unit, value in sens_data.items():
            if value is not False:
                options.append({"label": f"{unit}: {value}", "unit": unit, "value": value})
        return options

    def _on_sensitivity_combo_changed(self):
        """Handle SensitivityUnitCombo change.

        In DataBase mode the combo items ARE the sensitivity presets from
        the JSON, so selecting one also updates the value field and the
        tracked unit type.  In Custom mode the combo just selects the unit.
        """
        if self.ampType == 'DataBase' and self.SensitivityOptions:
            idx = self.SensitivityUnitCombo.currentIndex()
            if 0 <= idx < len(self.SensitivityOptions):
                opt = self.SensitivityOptions[idx]
                self.currentSensUnit = opt['unit']
                self.SensitivityValue.setText(str(opt['value']))
        self._recalculate()

    # ------------------------------------------------------------------
    # Core recalculation
    # ------------------------------------------------------------------

    def _recalculate(self, *args):
        if not self.AmpImpedanceComBoBox.isHidden():
            self.AmpImpedanceValue.setText(self.AmpImpedanceComBoBox.currentText())
            self.AmpPowerValue.setText(
                str(self.AmpData[self.OperationMode.currentText()]['Power'][self.AmpImpedanceComBoBox.currentIndex()])
            )
            # Sensitivity value is set by _on_sensitivity_combo_changed; don't overwrite it here.

        required = [
            self.SpeakerImpedanceValue.text(), self.SpeakerPowerValue.text(),
            self.AmpImpedanceValue.text(), self.AmpPowerValue.text(),
            self.SensitivityValue.text(), self.HPFValue.text(),
        ]
        self.ValueList = required + [self.LPFValue.text()]

        if '' in required:
            return

        try:
            [float(v) for v in required]
            self.allNumericValues = True
        except ValueError:
            self.allNumericValues = False

        if not self.allNumericValues:
            QMessageBox.warning(self, 'WARNING!', 'Please use only numerical values.', QMessageBox.Ok)
            return

        self.API.protect = float(self.ProtectionCombo.currentText())

        if self.HPFValue.text():
            self.API.setHPF(float(self.HPFValue.text()))
        if self.LPFValue.text():
            self.API.setLPF(float(self.LPFValue.text()))

        self.updateDriver(required[:2])
        self.updateAmp(required[2:])
        self.CalculateLimiters()
        self.updateGUIValues()

    def updateDriver(self, driver_values):
        self.driver.setImpedance(float(driver_values[0]))
        self.driver.setPower(float(driver_values[1]))
        self.driver.CalculateRMSPeakValues()
        self.API.setDriver(self.driver)

    def updateAmp(self, amp_values):
        self.amp.setImpedance(float(amp_values[0]))
        self.amp.setPower(float(amp_values[1]))
        self.amp.CalculateRMSPeakValues()

        # In DataBase mode the unit comes from the selected JSON option, not from
        # the combo text (which now shows a human-readable label, not a unit key).
        unit = self.currentSensUnit if self.ampType == 'DataBase' else self.SensitivityUnitCombo.currentText()

        if unit == 'V sens':
            self.amp.setVsens(float(amp_values[2]))
        elif unit == 'dBu sens':
            self.amp.setDBUSens(float(amp_values[2]))
        elif unit == 'X Factor':
            self.amp.setXfactor(float(amp_values[2]))
        elif unit == 'DB':
            self.amp.setDbGain(float(amp_values[2]))
        self.API.setAmp(self.amp)

    def CalculateLimiters(self):
        self.StoreParamsButton.setEnabled(True)
        self.API.calculatePeakLimiter()
        self.API.CalculateRMSLimiter()
        self.API.calculateTimeParameters()

    def changeAmpConfiguration(self):
        impedanceList = [str(z) for z in self.AmpData[self.OperationMode.currentText()]['Impedance']]
        self.AmpImpedanceComBoBox.clear()
        self.AmpImpedanceComBoBox.addItems(impedanceList)

    def updateGUIValues(self):
        self.AttackValue.setText(str(round(self.API.attack, 2)))
        self.ReleaseValue.setText(str(round(self.API.release, 2)))

        rms_unit = self.RMSThresholdUnitCombo.currentText()
        if rms_unit == 'dBu':
            self.RMSThresholdValue.setText(str(round(self.API.RMS_dBuTH, 2)))
        elif rms_unit.startswith('dBfs'):
            self.RMSThresholdValue.setText(str(round(self.API.RMS_dBuTH - 22, 2)))
        else:
            self.RMSThresholdValue.setText('not implemented yet')

        peak_unit = self.PeakThresholdUnitCombo.currentText()
        if peak_unit == 'dBu':
            self.PeakThresholdValue.setText(str(round(self.API.Peak_dBuTH, 2)))
        elif peak_unit.startswith('dBfs'):
            self.PeakThresholdValue.setText(str(round(self.API.Peak_dBuTH - 22, 2)))
        else:
            self.PeakThresholdValue.setText('not implemented yet')

        self.RMSThresholdValue.setEnabled(True)
        self.PeakThresholdValue.setEnabled(True)
        self.AttackValue.setEnabled(True)
        self.ReleaseValue.setEnabled(True)
        self.RMSThresholdValue.setReadOnly(True)
        self.PeakThresholdValue.setReadOnly(True)
        self.AttackValue.setReadOnly(True)
        self.ReleaseValue.setReadOnly(True)

    # ------------------------------------------------------------------
    # Dialog / load actions
    # ------------------------------------------------------------------

    def openAmpDialog(self):
        if self.ampType == 'Custom':
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            amp_db = str(_db_root() / 'dataBase' / 'amplifierDataBase')
            self.fileName, _ = QFileDialog.getOpenFileName(
                self, "Load Amplifier", directory=amp_db,
                filter="Amp file (*.json);;All Files (*)", options=options
            )
            if not self.fileName:
                return False

            with open(self.fileName, 'r') as f:
                self.AmpData = json.load(f)

            # Build sensitivity options and populate combo
            self.SensitivityOptions = self._load_sensitivity_options(self.AmpData['Sensitivity'])
            self.SensitivityUnitCombo.blockSignals(True)
            self.SensitivityUnitCombo.clear()
            for opt in self.SensitivityOptions:
                self.SensitivityUnitCombo.addItem(opt['label'])
            self.SensitivityUnitCombo.blockSignals(False)

            # Pre-select first sensitivity option
            if self.SensitivityOptions:
                first = self.SensitivityOptions[0]
                self.currentSensUnit = first['unit']
                self.SensitivityValue.setText(str(first['value']))

            # Populate OperationMode dynamically from JSON keys
            modes = [k for k in self.AmpData if k not in _AMP_META_KEYS]
            self.OperationMode.blockSignals(True)
            self.OperationMode.clear()
            self.OperationMode.addItems(modes)
            self.OperationMode.blockSignals(False)

            self.loadAmpButton.setText('Manual input')
            self.AmpImpedanceComBoBox.show()
            self.OperationMode.show()
            self.AmpImpedanceValue.setEnabled(False)
            self.AmpImpedanceValue.hide()
            self.AmpPowerValue.setEnabled(False)
            self.SensitivityValue.setEnabled(False)
            self.AmplificationInfoLabel.setText(
                'AmpData Data:  ' + self.AmpData['Brand'] + '-' + self.AmpData['Model']
            )
            impedanceList = [str(z) for z in self.AmpData[modes[0]]['Impedance']]
            self.AmpImpedanceComBoBox.clear()
            self.AmpImpedanceComBoBox.addItems(impedanceList)
            self.ampType = 'DataBase'
            self._recalculate()
            return True
        else:
            self.AmplificationInfoLabel.setText('Amplifier Characteristics')
            self.loadAmpButton.setText('Load amplifier')
            self.AmpImpedanceComBoBox.hide()
            self.OperationMode.hide()
            self.AmpImpedanceValue.show()
            self.AmpPowerValue.setEnabled(True)
            self.SensitivityValue.setEnabled(True)
            self.AmpImpedanceValue.setEnabled(True)
            self.ampType = 'Custom'

    def openDriverDialog(self):
        if self.driveType == 'Custom':
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            driver_db = str(_db_root() / 'dataBase' / 'driverDataBase')
            self.fileName, _ = QFileDialog.getOpenFileName(
                self, "Load Speaker", directory=driver_db,
                filter="Driver file (*.json);;All Files (*)", options=options
            )
            if not self.fileName:
                return False

            with open(self.fileName, 'r') as f:
                self.DriverData = json.load(f)

            self.loadDriverButton.setText('Manual input')

            self.driver.setPower(float(self.DriverData['Power']))
            self.SpeakerPowerValue.setText(str(self.driver.power))
            self.SpeakerPowerValue.setEnabled(False)

            self.driver.setImpedance(float(self.DriverData['Impedance']))
            self.SpeakerImpedanceValue.setText(str(self.driver.impedance))
            self.SpeakerImpedanceValue.setEnabled(False)

            self.SpeakerInfoLabel.setText(
                'Driver Data:  ' + self.DriverData['Brand'] + '-' + self.DriverData['Model']
            )
            self.driveType = 'DataBase'
            self._recalculate()
            return True
        else:
            self.SpeakerInfoLabel.setText('Speaker Characteristics')
            self.SpeakerPowerValue.setEnabled(True)
            self.SpeakerImpedanceValue.setEnabled(True)
            self.loadDriverButton.setText('Load Speaker')
            self.driveType = 'Custom'

    def storeParams(self):
        self.outputTable.setRowCount(self.row + 1)

        self.outputTable.setItem(self.row, 0, QTableWidgetItem(str(self.row + 1)))

        if self.ampType == 'Custom':
            self.outputTable.setItem(self.row, 1, QTableWidgetItem(' - '))
            self.outputTable.setItem(self.row, 2, QTableWidgetItem(' - '))
        else:
            self.outputTable.setItem(self.row, 1, QTableWidgetItem(self.AmpData['Brand'] + '-' + self.AmpData['Model']))
            self.outputTable.setItem(self.row, 2, QTableWidgetItem(self.OperationMode.currentText()))

        self.outputTable.setItem(self.row, 3, QTableWidgetItem(str(self.amp.power)))
        self.outputTable.setItem(self.row, 4, QTableWidgetItem(str(self.amp.impedance)))

        if self.driveType == 'Custom':
            self.outputTable.setItem(self.row, 5, QTableWidgetItem(' - '))
            self.outputTable.setItem(self.row, 6, QTableWidgetItem(' - '))
        else:
            self.outputTable.setItem(self.row, 5, QTableWidgetItem(self.DriverData['Brand'] + '-' + self.DriverData['Model']))
            self.outputTable.setItem(self.row, 6, QTableWidgetItem('TBD'))

        self.outputTable.setItem(self.row, 7, QTableWidgetItem(str(self.driver.power)))
        self.outputTable.setItem(self.row, 8, QTableWidgetItem(str(self.driver.impedance)))
        self.outputTable.setItem(self.row, 9, QTableWidgetItem(str(self.API.HPF)))
        self.outputTable.setItem(self.row, 10, QTableWidgetItem(str(self.API.LPF)))
        self.outputTable.setItem(self.row, 11, QTableWidgetItem(self.AttackValue.text()))
        self.outputTable.setItem(self.row, 12, QTableWidgetItem(self.ReleaseValue.text()))
        self.outputTable.setItem(self.row, 13, QTableWidgetItem(
            self.RMSThresholdValue.text() + ' ' + self.RMSThresholdUnitCombo.currentText()
        ))
        self.outputTable.setItem(self.row, 14, QTableWidgetItem(
            self.PeakThresholdValue.text() + ' ' + self.PeakThresholdUnitCombo.currentText()
        ))

        self.row += 1

    def resetParams(self):
        self.amp = amplifierBase()
        self.driver = speakerBase()

        for field in [self.SpeakerImpedanceValue, self.SpeakerPowerValue,
                      self.AmpImpedanceValue, self.AmpPowerValue,
                      self.SensitivityValue, self.RMSThresholdValue,
                      self.PeakThresholdValue, self.AttackValue,
                      self.ReleaseValue, self.HPFValue]:
            field.setText('')

        self.SpeakerInfoLabel.setText('')
        self.SpeakerPowerValue.setEnabled(True)
        self.SpeakerImpedanceValue.setEnabled(True)
        self.loadDriverButton.setText('Load Speaker')
        self.driveType = 'Custom'

        self.AmplificationInfoLabel.setText('')
        self.loadAmpButton.setText('Load amplifier')
        self.AmpImpedanceComBoBox.hide()
        self.OperationMode.hide()
        self.AmpImpedanceValue.show()
        self.AmpPowerValue.setEnabled(True)
        self.SensitivityValue.setEnabled(True)
        self.AmpImpedanceValue.setEnabled(True)
        self.ampType = 'Custom'

        # Restore default sensitivity combo items and state
        self.SensitivityOptions = []
        self.currentSensUnit = 'V sens'
        self.SensitivityUnitCombo.blockSignals(True)
        self.SensitivityUnitCombo.clear()
        self.SensitivityUnitCombo.addItems(_SENS_UNITS_DEFAULT)
        self.SensitivityUnitCombo.blockSignals(False)

        # Restore default operation mode items
        self.OperationMode.blockSignals(True)
        self.OperationMode.clear()
        self.OperationMode.addItems(_OP_MODES_DEFAULT)
        self.OperationMode.blockSignals(False)

        self.RMSThresholdValue.setEnabled(False)
        self.PeakThresholdValue.setEnabled(False)
        self.AttackValue.setEnabled(False)
        self.ReleaseValue.setEnabled(False)
        self.StoreParamsButton.setEnabled(False)
        self.allNumericValues = False


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import qdarktheme
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = LimiterApp()
    app.exec_()
