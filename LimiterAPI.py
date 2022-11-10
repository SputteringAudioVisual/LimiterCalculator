import math
from Utils.UnitConversor import DBConversor



class LimiterAPI:
    def __init__(self):
        self.amp = None
        self.driver = None
        self.protect = 0
        self.HPF = None


    def setAmp(self, amp):
        self.amp = amp

    def setDriver(self, driver):
        self.driver = driver

    def setHPF(self, hpf_value):
        self.HPF = hpf_value

    def CalculateRMSLimiter(self):
        if self.driver and self.amp:
            self.RMS_VoltageTH = (self.driver.V_RMS / self.amp.Xfactor) * (1 - (self.protect/100))
            self.RMS_dBuTH = DBConversor.V2DBU(self.RMS_VoltageTH)
            print('RMS limiter Threshold = ', self.RMS_dBuTH)


    def calculateTimeParameters(self):
        self.attack = 1000/self.HPF
        self.release = 15*self.attack


    def calculatePeakLimiter(self):
        self.Peak_VoltageTH = (self.driver.V_Peak / self.amp.Xfactor) * (1 - (self.protect/200))
        self.Peak_dBuTH = DBConversor.V2DBU(self.Peak_VoltageTH)
        print('Peak limiter Threshold = ', self.Peak_dBuTH)

