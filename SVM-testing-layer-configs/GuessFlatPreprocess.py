import os
import pandas as pd
import matplotlib
import librosa
import soundfile as sf
import matplotlib.pyplot as plt
import numpy as np
import librosa.display
import time

print(os.getcwd())

moozyc_path='./content/MyDrive/moozyc/'
genre_list=os.listdir(moozyc_path)
#genre_list

#['indian_indie','hindustani_classical','classic_bollywood','carnatic','desi_pop','tamil_pop','punjabi_hip_hop','ghazal','sufi','bhojpuri_pop']
data=[]
for genre in genre_list:
  genre_path='/'+genre
  music_files=os.listdir(moozyc_path+genre_path)
  music_files=[i  for i in music_files if i!='.spotdl-cache']
  
  #add each song to pandas df
  for song in music_files:
    song_path=moozyc_path+genre_path+'/'+song
    data.append([song_path,song,genre])

#creating pandas dataframe
song_df=pd.DataFrame(data,columns=['file_path','song','genre'])

#os.system('rm -rf ./content/spectrograms6sec')

#os.mkdir('./content/spectrograms6sec')
#for genre in genre_list:
  #os.mkdir(f'./content/spectrograms6sec/{genre}')

def save_spectrogram(block,sr,genre,song_name,counter):
  matplotlib.use('Agg')
  S = librosa.feature.melspectrogram(y=block, sr=sr, n_mels=128,fmax=8000)
  plt.figure(figsize=(6, 3))
  librosa.display.specshow(librosa.power_to_db(S,ref=np.max),y_axis='mel', fmax=8000,x_axis='time')
  # plt.plot()
  song_name=song_name.replace('.mp3','')
  file_name=f'./content/spectrograms6sec/{genre}/'+song_name+str(counter)+'.png'
  plt.savefig(file_name)
  plt.close()




def preprocess(file_name,song_name,genre):
  # First load the file
  try:
    audio, sr = librosa.load(file_name)


    # Get number of samples for 6 seconds; replace 2 by any number
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
      save_spectrogram(block,sr,genre,song_name,counter)
      # sf.write('1.wav', block, sr, 'PCM_24')
      counter += 1
      samples_wrote += buffer
  except:
    pass
  

    
      

for index,row in song_df.iterrows():
  if index<=330:
    start=time.time()

    preprocess(row["file_path"],row["song"],row["genre"])
    end=time.time()
    print(f"{row['song']} done",end-start,index)