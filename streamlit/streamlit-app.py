import os
import numpy as np
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import librosa
import testSong
import pandas as pd


import sys
sys.path.insert(0, '/home/amninder/Desktop/Folder_2')
st.set_page_config(page_title="sMartOx")


def smartox():
    
    st.markdown('# **sMartOx**')
    st.markdown('### _Music Genre Classifier and Recommender_')
    st.markdown('Check out source code at '
    '[Github](https://github.com/MadKauSing/SmartOx)')
    st.markdown('---')
    st.write('\n\n')

    #
    audio_bytes = audio_recorder()
    if audio_bytes:
        print("got audio")
        print(type(audio_bytes))
        st.audio(audio_bytes, format="audio/wav")
    
    if audio_bytes:
        os.system('rm -rf myfile.wav')

        with open('myfile.wav', mode='bx') as f:
            f.write(audio_bytes)
        
        genre_pred,ttd=testSong.testsong('myfile.wav')
        
        data={
            "Genres":[],
            "Confidence":[]
        }
        for x,y in ttd:
            data["Genres"].append(x)
            data["Confidence"].append(y)
        

        df=pd.DataFrame(data)
        st.table(df)
        st.markdown('### Your classification is')
        st.markdown(f'{genre_pred}')


    
    
    
    


smartox()

