
import os

#ml
import tensorflow as tf

#audio
import librosa
import librosa.display

import matplotlib
import matplotlib as plt

import numpy as np
from IPython.display import Audio

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

load_model=tf.keras.models.load_model


def save_spectrogram(block,sr,genre,song_name,counter):
  matplotlib.use('Agg')
  S = librosa.feature.melspectrogram(y=block, sr=sr, n_mels=128,fmax=8000)
  plt.figure(figsize=(6, 3))
  librosa.display.specshow(librosa.power_to_db(S,ref=np.max),y_axis='mel', fmax=8000,x_axis='time')
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
        save_spectrogram(block,sr,"classic_bollywood",song_name,counter)
        counter += 1
        samples_wrote += buffer


def save_spectrogram(block,sr,genre:str,song_name:str,counter:int):
  matplotlib.use('Agg')
  S = librosa.feature.melspectrogram(y=block, sr=sr, n_mels=128,fmax=8000)
  plt.figure(figsize=(6, 3))
  librosa.display.specshow(librosa.power_to_db(S,ref=np.max),y_axis='mel', fmax=8000,x_axis='time')
  # plt.plot()
  song_name=song_name.replace('.mp3','')
  file_name=f'testset/{genre}/'+song_name+str(counter)+'.png'
  plt.savefig(file_name)
  plt.close()


def ensemble_models(model_genres:list,model_input,model_input_cnn):

    #loading all models
    models=[]
    models.append(load_model('./models/model1/'))
    models.append(load_model('./models/model2/'))
    models.append(load_model('./models/model3/'))
    models.append(load_model('./models/model4/'))

    #prediction
    model1=models[0].predict(model_input)
    model2=models[1].predict(model_input)
    model3=models[2].predict(model_input)
    model4=models[3].predict(model_input_cnn)

    avgEnsemble=(model1+model2+model3+model4)/len(models)
    avgLis=[]
    for i in avgEnsemble:
        avgLis.append(i.argmax())
    confi_lis=avgEnsemble[0]
    
    for i in avgEnsemble[1:]:
        confi_lis+=i
    confi_lis=confi_lis/(len(avgEnsemble))
    summation=sum(confi_lis)
    #print(summation)

    text_to_display=[]
    for i in range(len(confi_lis)):
        acc=round(confi_lis[i]/summation,2)
        genr=model_genres[i]
        text_to_display.append([genr,acc])

    #print(avgLis)
    most_confi=max(avgLis,key=avgLis.count)
    most_prob_class=model_genres[most_confi]

    return most_prob_class,text_to_display


def testsong(file_path):

    genre_list=['bhojpuri_pop',
    'carnatic',
    'classic_bollywood',
    'desi_pop',
    'ghazal',
    'hindustani_classical',
    'indian_indie',
    'punjabi_hip_hop',
    'sufi',
    'tamil_pop']

    file_name=file_path
    filenameparts=file_name.split('/')
    song_name=filenameparts[-1]


    os.system('rm -rf testset')

    os.mkdir('testset')
    dest_path='testset'
    for genre in genre_list:
         os.mkdir(f'{dest_path}/{genre}')
    
    error=0
    try:
        audio, sr = librosa.load(file_name)
        make_spectrograms(audio,sr,song_name)

        data_dir_test='testset'

        #defining dataset dimensions
        batch_size=64
        image_height=100
        image_width=200

        #loading datasets

        test_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir_test,
        seed=123,
        image_size=(image_height, image_width),
        batch_size=batch_size,
        shuffle="False"
        )

        test_ds_cnn = tf.keras.utils.image_dataset_from_directory(
        data_dir_test,
        seed=123,
        image_size=(75, 150),
        batch_size=batch_size,
        shuffle="False"
        )

        genre_list=test_ds.class_names
        yhat_genre,ttd=ensemble_models(genre_list,test_ds,test_ds_cnn)
        return yhat_genre,ttd
    except:
        error=1
        return error,error
    

