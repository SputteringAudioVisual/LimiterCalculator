import math
from Utils.UnitConversor import DBConversor



class LimiterAPI:
    def __init__(self):
        self.amp = None
        self.driver = None
        self.protect = 0


    def setAmp(self, amp):
        self.amp = amp

    def setDriver(self, driver):
        self.driver = driver

    def CalculateRMSLimiter(self):
        if self.driver and self.amp:
            self.RMS_VoltageTH = (self.driver.V_RMS / self.amp.Xfactor) * (1 - (self.protect/100))
            self.RMS_dBuTH = DBConversor.V2DBU(self.RMS_VoltageTH)
            print('RMS limiter Threshold = ', self.RMS_dBuTH)


    def calculatePeakLimiter(self):
        self.Peak_VoltageTH = (self.driver.V_Peak / self.amp.Xfactor) * (1 - (self.protect/200))
        self.Peak_dBuTH = DBConversor.V2DBU(self.Peak_VoltageTH)
        print('Peak limiter Threshold = ', self.Peak_dBuTH)

