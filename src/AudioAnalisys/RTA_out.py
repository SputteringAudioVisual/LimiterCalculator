import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
from time import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"


import pyaudio
import wave
sound  = True
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100


p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output = True,
                output_device_index=5,
                frames_per_buffer=CHUNK)

fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'ro-')
frames = []


averagingTime = 0.1
averaged = [[], []]
start = time()
while stream.is_active():

    if time()-start<averagingTime:
        data = stream.read(CHUNK)
        audio_data = np.frombuffer(data, dtype=np.uint16)
        fft_data = np.fft.rfft(audio_data)  # rfft removes the mirrored part that fft generates
        fft_freq = np.fft.rfftfreq(len(audio_data), d=1 / RATE)  # rfftfreq needs the signal data, not the fft data
        ysmoothed = gaussian_filter1d(np.absolute(fft_data), sigma=2)
        averaged[0].append(fft_freq)
        averaged[1].append(ysmoothed)
    else:
        xValues = np.mean(averaged[0], axis=0)
        yValues = np.mean(averaged[1], axis=0)

        plt.plot(xValues, yValues- np.mean(yValues))
        plt.xscale('log')  # fft_data is a complex number, so the magnitude is computed here
        plt.yscale('log')
        plt.xlim(10, 20000)
        fig.canvas.draw()
        plt.pause(0.05)
        fig.canvas.flush_events()
        fig.clear()

        start=time()
        averaged = [[], []]







