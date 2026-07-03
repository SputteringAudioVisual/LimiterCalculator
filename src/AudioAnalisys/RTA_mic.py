import pyaudio
import numpy as np
import time
import matplotlib.animation as animation
from scipy.ndimage.filters import gaussian_filter1d
import matplotlib.pyplot as plt
from matplotlib import style
from time import time

pa = pyaudio.PyAudio()

callback_output = []

def callback(in_data, frame_count, time_info, flag):
    audio_data = np.fromstring(in_data, dtype=np.int16)
    print(np.max(audio_data))
    callback_output.append(audio_data)
    return None,pyaudio.paContinue


CHUNK = 1024
RATE = 44100
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=44100,
                 output=True,
                 input=True,
                 frames_per_buffer= CHUNK
                 )


stream.read(CHUNK)
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = ax.plot([], [], 'ro-')
frames = []
averagingTime = 0.1
averaged = [[], []]
start = time()

while stream.is_active():

    if time()-start<averagingTime:
        audio_data = np.frombuffer(stream.read(CHUNK) , dtype=np.uint32)

        fft_data = np.fft.rfft(audio_data)  # rfft removes the mirrored part that fft generates
        fft_freq = np.fft.rfftfreq(len(audio_data), d=1 / RATE)  # rfftfreq needs the signal data, not the fft data
        ysmoothed = gaussian_filter1d(np.absolute(fft_data), sigma=2)
        averaged[0].append(fft_freq)
        averaged[1].append(ysmoothed)
    else:
        xValues = np.mean(averaged[0], axis=0)
        yValues = np.mean(averaged[1], axis=0)

        plt.plot(xValues, yValues)
        # fft_data is a complex number, so the magnitude is computed here

        plt.xlim(1, 20000)
        fig.canvas.draw()
        plt.pause(0.05)
        fig.canvas.flush_events()
        fig.clear()

        start=time()
        averaged = [[], []]