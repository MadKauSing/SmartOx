import os

import PIL.Image
import tensorflow as tf
import librosa

import matplotlib
import matplotlib as plt

from matplotlib import figure

import numpy as np
from IPython.display import Audio

from tensorflow.keras.models import load_model
import pathlib
import loadsong

import tensorflow
load_model=tensorflow.keras.models.load_model

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
    #print(confi_lis)
    summation=sum(confi_lis)


    text_to_display=[]

    for i in range(len(confi_lis)):
        acc=round(confi_lis[i]/summation,2)
        genr=model_genres[i]

        strin=f"{genr}\t\t\t\t{acc}%"
        text_to_display.append([genr,acc])
        print(strin.rjust(50,' '))


    #print(avgLis)
    most_confi=max(avgLis,key=avgLis.count)
    most_prob_class=model_genres[most_confi]

    return most_prob_class,text_to_display


def testsong(file_path):
    test_path='testset/'

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
    song_name

    os.system('rm -rf testset')

    os.mkdir('testset')
    dest_path='testset'

    for genre in genre_list:
         os.mkdir(f'{dest_path}/{genre}')
    audio, sr = librosa.load(file_name)

    Audio(data=audio, rate=sr)

    loadsong.make_spectrograms(audio,sr,song_name)

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
    print(yhat_genre)
    return yhat_genre,ttd

