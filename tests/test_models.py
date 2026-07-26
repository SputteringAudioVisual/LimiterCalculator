import math
import unittest

from amplifiers.AmplifierBase import amplifierBase
from Speakers.SpeakerBase import speakerBase
from src.API.LimiterAPI import LimiterAPI
from Utils.UnitConversor import DBConversor


class UnitConversionTests(unittest.TestCase):
    def test_dbu_reference_is_approximately_0775_volts(self):
        self.assertAlmostEqual(DBConversor.DBU2V(0), 0.7746, places=4)

    def test_dbu_round_trip(self):
        for value in (-10, 0, 4, 22, 32):
            with self.subTest(value=value):
                self.assertAlmostEqual(
                    DBConversor.V2DBU(DBConversor.DBU2V(value)),
                    value,
                    places=9,
                )


class ElectricalModelTests(unittest.TestCase):
    def test_amplifier_rms_and_peak_values(self):
        amplifier = amplifierBase()
        amplifier.setPower(1000)
        amplifier.setImpedance(4)
        amplifier.CalculateRMSPeakValues()

        self.assertAlmostEqual(amplifier.V_RMS, math.sqrt(4000), places=9)
        self.assertAlmostEqual(
            amplifier.V_Peak,
            amplifier.V_RMS * math.sqrt(2),
            places=9,
        )

    def test_limiter_chain(self):
        amplifier = amplifierBase()
        amplifier.setPower(1000)
        amplifier.setImpedance(4)
        amplifier.CalculateRMSPeakValues()
        amplifier.setDbGain(32)

        speaker = speakerBase()
        speaker.setPower(500)
        speaker.setImpedance(8)
        speaker.CalculateRMSPeakValues()

        limiter = LimiterAPI()
        limiter.setAmp(amplifier)
        limiter.setDriver(speaker)
        limiter.setHPF(40)
        limiter.protect = 10
        limiter.CalculateRMSLimiter()
        limiter.calculatePeakLimiter()
        limiter.calculateTimeParameters()

        expected_rms_input = speaker.V_RMS / amplifier.Xfactor
        expected_peak_input = speaker.V_Peak / amplifier.Xfactor
        self.assertAlmostEqual(
            limiter.RMS_VoltageTH,
            expected_rms_input * 0.9,
            places=9,
        )
        self.assertAlmostEqual(
            limiter.Peak_VoltageTH,
            expected_peak_input * 0.95,
            places=9,
        )
        self.assertAlmostEqual(limiter.attack, 25.0, places=9)
        self.assertAlmostEqual(limiter.release, 375.0, places=9)


if __name__ == "__main__":
    unittest.main()
