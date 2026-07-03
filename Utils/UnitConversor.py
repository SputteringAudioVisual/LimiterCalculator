import math
class DBConversor:
    dBu_ref = 0.7746    # voltios
    dBv_ref = 1
    def __init__(self):
        pass

    @classmethod
    def DBU2V(cls, dbu):
        return cls.dBu_ref * (10**(dbu/20))

    @classmethod
    def V2DBU(cls, volts):
        return 20*math.log10(volts/cls.dBu_ref)


