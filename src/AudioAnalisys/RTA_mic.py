import pyaudio
import numpy as np
import time
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import style

pa = pyaudio.PyAudio()

callback_output = []

def callback(in_data, frame_count, time_info, flag):
    audio_data = np.fromstring(in_data, dtype=np.int16)
    print(np.max(audio_data))
    callback_output.append(audio_data)
    return None,pyaudio.paContinue



stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=44100,
                 output=False,
                 input=True,
                 stream_callback=callback)

stream.start_stream()
while True:
    pass