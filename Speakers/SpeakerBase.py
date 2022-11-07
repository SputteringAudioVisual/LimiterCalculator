import math
class speakerBase:

    DutyFactor = 2
    def __init__(self):
        self.power = None
        self.impedance = None

        self.V_RMS = None
        self.I_RMS = None
        self.V_Peak = None
        self.I_Peak = None


    def setImpedance(self, impedance):
        self.impedance = impedance

    def setPower(self, power):
        self.power = power

    def CalculateRMSPeakValues(self):
        self.I_RMS = math.sqrt(self.power / self.impedance)
        self.V_RMS = self.I_RMS * self.impedance

        self.I_Peak = self.I_RMS * self.DutyFactor
        self.V_Peak = self.V_RMS * self.DutyFactor