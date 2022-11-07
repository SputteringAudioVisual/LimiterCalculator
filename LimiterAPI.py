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

    sens_amp = 1.228
    P_amp = 200
    R_amp = 8

    P_speakers = 100
    R_speakers = 8


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

    print(Ipeak_speaker, VPeak_speaker)
    print(Ipeak_amp, Vpeak_amp)


    # una vez hemos obtenido las corrientes y tensiones maximas y rms que se van a producir en el amp y que se pueden
    # soportar por parte de el altavoz, hemos de emplear el factorX de la etapa para asegurarnos que el voltaje y
    # corriente RMS desarollador pos la etapa no exceden a lo que el cono puede aceptar


    Xfactor = Vrms_amp/sens_amp
    print('X factor = ', Xfactor)

    # Copn este factor de multiplicacion, vamos a calcular el voltaje maximo a la entrada para que la salida no exceda
    # la tension que puede admitir el cono.

    Vin_max = Vrms_speaker/Xfactor


    # UNa vez tenemos la tension maxima de entrada expresada en voltios, la pasamos a dbu

    DBin_max=DBConversor.V2DBU(Vin_max)

    print('max dbu in:', DBin_max)


    # calculado el nivel maximo de entrada para no cargarnos el altavoz, hemos de calcular el threshold del limitador
    # primro definimos un factor de proteccion entra 0 y 1
    protect = 0.5
    Vumbral  =(Vrms_speaker/Xfactor)*(1-protect)
    DBUUmbral = DBConversor.V2DBU(Vumbral)
    print('dbUmbral = ', DBUUmbral)