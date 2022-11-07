import math
from Utils.UnitConversor import DBConversor
class amplifierBase:
    DutyFactor = math.sqrt(2)
    def __init__(self):
        self.power = None
        self.impedance = None

        self.Vsensitivity = None
        self.dBuSensitivity = None
        self.Xfactor = None
        self.gain = None
        self.SensType = None

        self.V_RMS = None
        self.I_RMS = None
        self.V_Peak = None
        self.I_Peak = None



    def setPower(self, power):
        self.power = power

    def setImpedance(self, impedance):
        self.impedance = impedance

    def CalculateRMSPeakValues(self):
        self.I_RMS = math.sqrt(self.power/self.impedance)
        self.V_RMS = self.I_RMS * self.impedance

        self.I_Peak = self.I_RMS * self.DutyFactor
        self.V_Peak = self.V_RMS * self.DutyFactor


    def setVsens(self,Vsens):
        self.Vsensitivity = Vsens
        self.dBuSensitivity = DBConversor.V2DBU(Vsens)
        self.Xfactor = self.V_RMS/self.Vsensitivity


