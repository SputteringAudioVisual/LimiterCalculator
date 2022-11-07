import math
from Utils.UnitConversor import DBConversor
from amplifiers.AmplifierBase import amplifierBase
from Speakers.SpeakerBase import speakerBase
from LimiterAPI import LimiterAPI


amp = amplifierBase()
amp.setPower(200)
amp.setImpedance(8)
amp.CalculateRMSPeakValues()
amp.setVsens(1.22)



driver = speakerBase()
driver.setImpedance(8)
driver.setPower(100)
driver.CalculateRMSPeakValues()

limiter = LimiterAPI()

limiter.setAmp(amp)
limiter.setDriver(driver)


limiter.CalculateRMSLimiter()

limiter.calculatePeakLimiter()
