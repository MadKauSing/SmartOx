import os
import pandas as pd
import matplotlib
import librosa
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import librosa.display
import time

import os




def save_spectrogram(block,sr,genre,song_name,counter):
  matplotlib.use('Agg')
  S = librosa.feature.melspectrogram(y=block, sr=sr, n_mels=128,fmax=8000)
  plt.figure(figsize=(6, 3))
  librosa.display.specshow(librosa.power_to_db(S,ref=np.max),y_axis='mel', fmax=8000,x_axis='time')
  # plt.plot()
  song_name=song_name.replace('.mp3','')
  file_name=f'testset/{genre}/'+song_name+str(counter)+'.png'
  plt.savefig(file_name)
  plt.close()



def make_spectrograms(audio,sr,song_name):
    buffer = 6 * sr

    samples_total = len(audio)
    samples_wrote = 0
    counter = 1

    while samples_wrote < samples_total: 
        #check if the buffer is not exceeding total samples 
        if buffer > (samples_total - samples_wrote):
            buffer = samples_total - samples_wrote

        block = audio[samples_wrote : (samples_wrote + buffer)]
        # Write 2 second segment
        save_spectrogram(block,sr,"classic_bollywood",song_name,counter)

        counter += 1
        samples_wrote += buffer

