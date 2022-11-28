import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d

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
RECORD_SECONDS = 1000
WAVE_OUTPUT_FILENAME = "output.wav"


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




while stream.is_active():
    data = stream.read(CHUNK)
    audio_data = np.frombuffer(data, dtype=np.uint16)
    fft_data = np.fft.rfft(audio_data)  # rfft removes the mirrored part that fft generates
    fft_freq = np.fft.rfftfreq(len(audio_data), d=1 / RATE)  # rfftfreq needs the signal data, not the fft data

    ysmoothed = gaussian_filter1d(np.absolute(fft_data), sigma=2)


    plt.plot(fft_freq, ysmoothed)
    plt.xscale('log')# fft_data is a complex number, so the magnitude is computed here
    plt.yscale('log')
    plt.xlim(np.amin(fft_freq), np.amax(fft_freq))
    plt.ylim([-1E+7, 2E+7])
    fig.canvas.draw()
    plt.pause(0.05)
    fig.canvas.flush_events()
    fig.clear()