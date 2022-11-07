import math
from Utils.UnitConversor import DBConversor



class LimiterAPI:
    def __init__(self):
        self.amp = None
        self.driver = None
        self.protect = 0.5


    def setAmp(self, amp):
        self.amp = amp

    def setDriver(self, driver):
        self.driver = driver

    def CalculateRMSLimiter(self):
        if self.driver and self.amp:
            VUmbral_RMS = (self.driver.V_RMS / self.amp.Xfactor) * (1 - self.protect)
            LimiterTH_RMS = DBConversor.V2DBU(VUmbral_RMS)
            print('RMS limiter Threshold = ', LimiterTH_RMS)
        else:
            print('set driver an amp  before')

    def calculatePeakLimiter(self):
        VUmbral_Peak = (self.driver.V_Peak / self.amp.Xfactor) * (1 - (self.protect/2))
        LimiterTH_Peak = DBConversor.V2DBU(VUmbral_Peak)
        print('RMS limiter Threshold = ', LimiterTH_Peak)
