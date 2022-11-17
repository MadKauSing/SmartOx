from PIL import Image
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from IPython.display import Audio
from tensorflow.keras.models import load_model
from PIL import Image
from scipy import spatial

def get_image_array(image):
    img = image.resize((100,200))
    img_arr = np.array(img)
    img_arr = img_arr.flatten()
    img_arr = img_arr/255
    return img_arr

def get_song_name(img_name):
    return ''.join((x for x in img_name[:-4] if not x.isdigit()))

def get_recommendations(song,yhat):
    dest_path = "../content/new/spectrograms6secnew"
    compared_image = get_image_array(song)
    similarity_images = []
    path = os.path.join(dest_path,yhat)
    
    for images in os.listdir(path):
        image_obj = Image.open(os.path.join(path,images))
        
        image2 = get_image_array(image_obj)
        similarity = -1 * (spatial.distance.cosine(compared_image,image2) - 1)
        image_name = images.split('\\')[-1]
        song_name = get_song_name(image_name)
        
        prev_song_name = song_name
        similarity_images.append([song_name,similarity])
        df = pd.DataFrame(similarity_images,columns=["Name","Score"])
        avgeraged_similarities = df.groupby('Name').mean('Score').reset_index()
        suggestions = avgeraged_similarities.sort_values('Score',ascending=False).head(10)
        # suggestions = df.sort_values('Score',ascending=False).head(10)
        return suggestions