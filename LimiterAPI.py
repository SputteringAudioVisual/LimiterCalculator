import math

class DBConversor:
    def __init__(self):
        pass

    @staticmethod
    def DBU2V(dbu):
        return 0.775 * (10**(dbu/20))

    @staticmethod
    def V2DBU(volts):
        return 20*math.log10(volts/0.775)

class LmiterAPI:
    def __init__(self):
        pass





if __name__ == "__main__":
    Cresta_amp_seno = math.sqrt(2)
    Cresta_speaker_ruido = 1/0.5


    sens_amp = float(input('please enter you amplifier sensitivity (V)'))
    P_amp = float(input('Please enter your amplifier power'))
    R_amp = float(input('Please eneter your amplifier impedance'))

    P_speakers = float(input('Please enter your speaker RMS power consumption'))
    R_speakers = float(input('please enter your speaker impedance'))

    protect = 50


    #comenzamos calculando las corriente y tensiones pico. Para ello, usamos la ley de hom sobre los valores nominales
    # CorrienteRMS = raiz(potencia/resistencia)
    # VoltajeRMS = CorrienteRMS*Resistencia
    # CorrientePico = CorrienteRMS*FactorDeCrestaç
    # VoltajePico = VoltajeRMS*FactorDeCresta



    Irms_amp = math.sqrt(P_amp/R_amp)
    Vrms_amp = Irms_amp*R_amp
    Ipeak_amp = Irms_amp* Cresta_amp_seno
    Vpeak_amp = Vrms_amp*Cresta_amp_seno


    Irms_speaker = math.sqrt(P_speakers/R_speakers)
    Vrms_speaker = Irms_speaker*R_speakers
    Ipeak_speaker = Irms_speaker*Cresta_speaker_ruido
    VPeak_speaker = Vrms_speaker*Cresta_speaker_ruido


    # una vez hemos obtenido las corrientes y tensiones maximas y rms que se van a producir en el amp y que se pueden
    # soportar por parte de el altavoz, hemos de emplear el factorX de la etapa para asegurarnos que el voltaje y
    # corriente RMS desarollador pos la etapa no exceden a lo que el cono puede aceptar
    Xfactor = Vrms_amp/sens_amp


    # Copn este factor de multiplicacion, vamos a calcular el voltaje maximo a la entrada para que la salida no exceda
    # la tension que puede admitir el cono.

    VInMax_RMS = Vrms_speaker / Xfactor


    # UNa vez tenemos la tension maxima de entrada expresada en voltios, la pasamos a dbu

    dBuInMax_RMS=DBConversor.V2DBU(VInMax_RMS)




    # calculado el nivel maximo de entrada para no cargarnos el altavoz, hemos de calcular el threshold del limitador
    # primro definimos un factor de proteccion entra 0 y 1
    protect = 0.5
    VUmbral_RMS  = (Vrms_speaker / Xfactor) * (1 - protect)
    LimiterTH_RMS = DBConversor.V2DBU(VUmbral_RMS)
    print('RMS limiter Threshold = ', LimiterTH_RMS)


    '--------------'

    VInMax_Peak = VPeak_speaker/Xfactor
    # UNa vez tenemos la tension maxima de entrada expresada en voltios, la pasamos a dbu

    dBuInMax_Peak = DBConversor.V2DBU(VInMax_Peak)

    # calculado el nivel maximo de entrada para no cargarnos el altavoz, hemos de calcular el threshold del limitador
    # primro definimos un factor de proteccion entra 0 y 1

    VUmbral_Peak = (VPeak_speaker/Xfactor)*(1-(protect/2))
    LimiterTH_Peak = DBConversor.V2DBU(VUmbral_Peak)
    print('Peak limiter Threshold = ', LimiterTH_Peak)

