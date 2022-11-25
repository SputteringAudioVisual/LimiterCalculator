from scipy.io import wavfile
import  matplotlib.pyplot as plt
import os
from pathlib import Path
import numpy as np

filePath = Path(os.getcwd()).parent.parent / Path(r'Utils/1KHz_192KHz_24bit_60sec_0db.wav')
data = wavfile.read(filePath)
audio = data[1]

audio1 = audio[0:1000]
audio2 = audio[100:1100]

fft1 = np.fft.fftfreq(audio1.size, audio1)
fft2 = np.fft.fftfreq(audio2.size,audio2)

plt.figure()
plt.plot(audio1)
plt.plot(audio2)

plt.figure()
plt.xlim([0, 20000])
plt.magnitude_spectrum(audio1, Fs=192000, scale='dB', color='C1')

plt.show()